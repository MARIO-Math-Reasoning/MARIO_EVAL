from typing import Optional, Tuple, Union

from .latex_normalize import (
    string_normalize,
    split_tuple,
    split_matrix,
    _is_frac, 
    _str_is_int,
    _str_is_mat,
    _str_to_mat,
    _str_to_interval,
)
from .latex_parser import are_equal_under_sympy
from .constants import EPSILON
import sympy


def is_equiv(ground_truth: str, given: str, verbose: bool = False, fast: bool = False):
    if ground_truth is None and given is None:
        print("WARNING: Both None")
        return True
    if ground_truth is None or given is None:
        return False

    str_pass = ground_truth.strip() == given.strip()
    if str_pass:
        return True

    def default_is_equiv(ground_truth_normalized: Union[str, set], given_normalized: Union[str, set]) -> bool:
        if verbose:
            print(ground_truth_normalized, given_normalized)

        if isinstance(ground_truth_normalized, str) and ground_truth_normalized == given_normalized:
            return True

        try:
            # e.g., gt = 30^\\circ -> {30, pi/6}, gv = pi/6
            if isinstance(ground_truth_normalized, set) or isinstance(given_normalized, set):
                if isinstance(ground_truth_normalized, str):
                    ground_truth_normalized = {ground_truth_normalized}
                if isinstance(given_normalized, str):
                    given_normalized = {given_normalized}
                for gt_norm in ground_truth_normalized:
                    for gv_norm in given_normalized:
                        if is_latex_equiv(gt_norm, gv_norm, verbose=verbose):
                            return True
                return False
            else:
                return is_latex_equiv(ground_truth_normalized, given_normalized, verbose=verbose)

        except Exception as e:
            return False 

    ground_truth_normalized = string_normalize(ground_truth)
    given_normalized = string_normalize(given)
    default_equiv = default_is_equiv(ground_truth_normalized, given_normalized)

    if fast or default_equiv:
        return default_equiv
    else:
        ground_truth_normalized = string_normalize(ground_truth, remove_mid_std_space=False)
        given_normalized = string_normalize(given, remove_mid_std_space=False)
        default_equiv_space = default_is_equiv(ground_truth_normalized, given_normalized)
        if default_equiv_space:
            return True
        
        ground_truth_normalized = string_normalize(ground_truth, lower_case=False)
        given_normalized = string_normalize(given, lower_case=False)
        default_equiv_case = default_is_equiv(ground_truth_normalized, given_normalized)
        if default_equiv_case:
            return True
        
        raw_equiv = are_equal_under_sympy(ground_truth, given)
        return raw_equiv


def is_latex_equiv(
    ground_truth_normalized: str, 
    given_normalized: str, 
    verbose: bool = False,
) -> bool:
    if len(given_normalized) == 0:
        return False

    is_correct, splitted = False, False
    if '(' in ground_truth_normalized or ')' in ground_truth_normalized or '[' in ground_truth_normalized or ']' in ground_truth_normalized:
        is_correct, splitted = is_equiv_possible_intervals(ground_truth_normalized, given_normalized, verbose)
    
    if not is_correct:
        is_correct, splitted = is_equiv_possible_tuple(ground_truth_normalized, given_normalized, verbose)

    if not is_correct and (_str_is_mat(ground_truth_normalized) or _str_is_mat(given_normalized)):
        is_correct, splitted = is_equiv_possible_matrix(ground_truth_normalized, given_normalized, verbose)

    if not is_correct and not splitted:
        is_correct = are_equal_under_sympy(ground_truth_normalized, given_normalized, verbose)
    
    return is_correct


def is_equiv_possible_intervals(
    ground_truth_normalized: str, 
    given_normalized: str, 
    verbose: bool = False,
) -> Tuple[bool, bool]:
    gt_interval = _str_to_interval(ground_truth_normalized)
    gv_interval = _str_to_interval(given_normalized)

    splitted = True
    if gt_interval is None and gv_interval is None:
        splitted = False

    if gt_interval is not None and gv_interval is not None and gt_interval.compare(gv_interval) == 0:
        return True, splitted

    return False, splitted


def is_equiv_possible_tuple(
    ground_truth_normalized: str, 
    given_normalized: str, 
    verbose: bool = False,
) -> Tuple[bool, bool]:
    # split "(,,,)" or "[,,,]" into list, split ",,," into set
    ground_truth_elems = split_tuple(ground_truth_normalized)
    given_elems = split_tuple(given_normalized)

    if verbose:
        print(ground_truth_elems, given_elems)

    splitted = True
    if isinstance(ground_truth_elems, str) and isinstance(given_elems, str):
        if ground_truth_elems == ground_truth_normalized and given_elems == given_normalized:
            return False, False
        else:
            return is_equiv(ground_truth_elems, given_elems, verbose), splitted

    is_correct = False
    if len(ground_truth_elems) != len(given_elems) and not '\\in' in given_elems:
        is_correct = False
    elif type(ground_truth_elems) != type(given_elems):
        is_correct = False
    elif isinstance(ground_truth_elems, (list, tuple)):
        for ground_truth_elem, given_elem in zip(ground_truth_elems, given_elems):
            if not is_equiv(ground_truth_elem, given_elem, verbose):
                return False, splitted
        return True, splitted
    elif isinstance(ground_truth_elems, set):
        gt_found_matches = [False] * len(ground_truth_elems)
        gv_found_matches = [False] * len(given_elems)
        for i, ground_truth_elem in enumerate(ground_truth_elems):
            if not gt_found_matches[i]:
                for j, given_elem in enumerate(given_elems):
                    if not gv_found_matches[j] and is_equiv(ground_truth_elem, given_elem, verbose):
                        gt_found_matches[i] = True
                        gv_found_matches[j] = True
                        break
        return all(gt_found_matches), splitted

    return is_correct, splitted


def is_equiv_possible_matrix(
    ground_truth_normalized: str, 
    given_normalized: str, 
    verbose: bool = False,
) -> Tuple[bool, bool]:
    gt_matrix = split_matrix(ground_truth_normalized)
    gv_matrix = split_matrix(given_normalized)
    
    splitted = True
    if isinstance(gt_matrix, str) and isinstance(gv_matrix, str):
        if gt_matrix == ground_truth_normalized and gv_matrix == given_normalized:
            return False, False
        else:
            return is_equiv(gt_matrix, gv_matrix), splitted

    elif isinstance(gt_matrix, list) and isinstance(gv_matrix, list):
        # check num of rows are equal
        if len(gt_matrix) != len(gv_matrix):
            return False, splitted

        for gt_col, gv_col in zip(gt_matrix, gv_matrix):
            if isinstance(gt_col, str) and isinstance(gv_col, str) and is_equiv(gt_col, gv_col):
                continue

            elif isinstance(gt_col, list) and isinstance(gv_col, list):
                # check num of cols are equal
                if len(gt_col) != len(gv_col):
                    return False, splitted

                for gt_col_item, gv_col_item in zip(gt_col, gv_col):
                    if not is_equiv(gt_col_item, gv_col_item):
                        return False, splitted
            else:
                return False, splitted

        return True, splitted
                
    else:
        return False, splitted
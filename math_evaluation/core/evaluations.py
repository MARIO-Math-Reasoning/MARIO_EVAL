from typing import Optional

from .latex_normalize import (
    string_normalize,
    split_tuple,
    split_matrix,
    _is_frac, 
    _str_is_int,
    _str_is_mat,
    _str_to_mat,
    _str_to_list,
    _str_to_interval,
)
from .latex_parser import are_equal_under_sympy
from .constants import EPSILON
import sympy


def is_equiv(ground_truth: str, given: str, verbose: bool = False):
    if ground_truth is None and given is None:
        print("WARNING: Both None")
        return True
    if ground_truth is None or given is None:
        return False
    
    str_pass, ground_truth_normalized, given_normalized = is_normalized_string_equival(ground_truth, given, verbose=verbose)
    if str_pass:
        return True

    try:
        if isinstance(ground_truth_normalized, set):
            for gr_norm in ground_truth_normalized:
                if is_latex_equiv(gr_norm, given_normalized, verbose=verbose):
                    return True
            return False
        else:
            return is_latex_equiv(ground_truth_normalized, given_normalized, verbose=verbose)

    except Exception as e:
        return False 


def is_normalized_string_equival(ground_truth: str, given: str, verbose: bool = False):
    try:
        ground_truth_normalized = string_normalize(ground_truth, is_ground_truth=True)
        given_normalized = string_normalize(given)
        if verbose:
            print(ground_truth_normalized, given_normalized)
        if isinstance(ground_truth_normalized, str):
            if ground_truth_normalized == given_normalized:
                return True, ground_truth_normalized, given_normalized
        return ground_truth_normalized == given_normalized, ground_truth_normalized, given_normalized
    except:
        return ground_truth == given, ground_truth, given


def is_latex_equiv(
    ground_truth_normalized: str, 
    given_normalized: str, 
    verbose: bool = False,
) -> bool:
    if len(given_normalized) == 0:
        return False

    is_correct = False
    if '(' in ground_truth_normalized or ')' in ground_truth_normalized or '[' in ground_truth_normalized or ']' in ground_truth_normalized:
        is_correct = is_equiv_possible_intervals(ground_truth_normalized, given_normalized, verbose)
    
    if not is_correct:
        is_correct = is_equiv_possible_tuple(ground_truth_normalized, given_normalized, verbose, known_equiv=False)

    if not is_correct:
        is_correct = is_equiv_possible_matrix(ground_truth_normalized, given_normalized, verbose, known_equiv=False)

    # expr startswith [ or (, endwiths ) or ] are evaluated in above cases
    gt_done = len(ground_truth_normalized) >= 2 and ground_truth_normalized[0] + ground_truth_normalized[-1] in ["[]", "()", "{}"]
    gv_done = len(given_normalized) >= 2 and given_normalized[0] + given_normalized[-1] in ["[]", "()", "{}"]
    if not is_correct and (not gt_done or not gv_done):
        is_correct = are_equal_under_sympy(ground_truth_normalized, given_normalized, verbose)
    
    return is_correct


def is_equiv_possible_intervals(
    ground_truth_normalized: str, 
    given_normalized: str, 
    verbose: bool = False,
) -> bool:
    gt_interval = _str_to_interval(ground_truth_normalized)
    gv_interval = _str_to_interval(given_normalized)
    if gt_interval is not None and gv_interval is not None and sympy.Eq(gt_interval, gv_interval):
        return True
    return False


def is_equiv_possible_tuple(
    ground_truth_normalized: str, 
    given_normalized: str, 
    verbose: bool = False,
    known_equiv: Optional[bool] = None,
) -> bool:
    # split "(,,,)" or "[,,,]" into list, split ",,," into set
    ground_truth_elems = split_tuple(ground_truth_normalized)
    given_elems = split_tuple(given_normalized)

    if verbose:
        print(ground_truth_elems, given_elems)

    if isinstance(ground_truth_elems, str) and isinstance(given_elems, str):
        if known_equiv is None or ground_truth_elems != ground_truth_normalized or given_elems != given_normalized:
            return is_equiv(ground_truth_elems, given_elems)
        else:
            return known_equiv

    is_correct = False
    if len(ground_truth_elems) != len(given_elems) and not '\\in' in given_elems:
        is_correct = False
    elif type(ground_truth_elems) != type(given_elems):
        is_correct = False
    elif isinstance(ground_truth_elems, (list, tuple)):
        for ground_truth_elem, given_elem in zip(ground_truth_elems, given_elems):
            if not is_equiv(ground_truth_elem, given_elem):
                return False
        return True
    elif isinstance(ground_truth_elems, set):
        gt_found_matches = [False] * len(ground_truth_elems)
        gv_found_matches = [False] * len(given_elems)
        for i, ground_truth_elem in enumerate(ground_truth_elems):
            if not gt_found_matches[i]:
                for j, given_elem in enumerate(given_elems):
                    if not gv_found_matches[j] and is_equiv(ground_truth_elem, given_elem):
                        gt_found_matches[i] = True
                        gv_found_matches[j] = True
                        break
        return all(gt_found_matches)

    return is_correct


def is_equiv_possible_matrix(
    ground_truth_normalized: str, 
    given_normalized: str, 
    verbose: bool = False,
    known_equiv: Optional[bool] = None,
) -> bool:
    gt_matrix = split_matrix(ground_truth_normalized)
    gv_matrix = split_matrix(given_normalized)
    
    if isinstance(gt_matrix, str) and isinstance(gv_matrix, str):
        if known_equiv is None or gt_matrix != ground_truth_normalized or gv_matrix != given_normalized:
            return is_equiv(gt_matrix, gv_matrix)
        else:
            return known_equiv

    elif isinstance(gt_matrix, list) and isinstance(gv_matrix, list):
        # check num of rows are equal
        if len(gt_matrix) != len(gv_matrix):
            return False

        for gt_col, gv_col in zip(gt_matrix, gv_matrix):
            if isinstance(gt_col, str) and isinstance(gv_col, str) and is_equiv(gt_col, gv_col):
                continue

            elif isinstance(gt_col, list) and isinstance(gv_col, list):
                # check num of cols are equal
                if len(gt_col) != len(gv_col):
                    return False

                for gt_col_item, gv_col_item in zip(gt_col, gv_col):
                    if not is_equiv(gt_col_item, gv_col_item):
                        return False
            else:
                return False

        return True
                
    else:
        return False
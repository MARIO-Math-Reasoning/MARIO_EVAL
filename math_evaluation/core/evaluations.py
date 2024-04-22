import re

from .latex_normalize import (
    string_normalize,
    split_tuple,
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

    except Exception as e:  # 捕获任何异常，并将其绑定到变量 e
        return False  # 发生异常时返回 False


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

    is_correct = are_equal_under_sympy(ground_truth_normalized, given_normalized, verbose)
    if is_correct:
        return True

    is_correct = False
    if '(' in ground_truth_normalized or ')' in ground_truth_normalized or '[' in ground_truth_normalized or ']' in ground_truth_normalized:
        is_correct = is_equiv_possible_intervals(ground_truth_normalized, given_normalized, verbose)
    
    if not is_correct:
        is_correct = is_equiv_possible_tuple(ground_truth_normalized, given_normalized, verbose)
    
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
) -> bool:
    # split "(,,,)" or "[,,,]" into list, split ",,," into set
    ground_truth_elems = split_tuple(ground_truth_normalized)
    gt_type = type(ground_truth_elems)
    given_elems = split_tuple(given_normalized, expect_type=gt_type)

    if verbose:
        print(ground_truth_elems, given_elems)

    is_correct = False
    if len(ground_truth_elems) != len(given_elems) and not '\\in' in given_elems:
        is_correct = False
    elif type(ground_truth_elems) != type(given_elems):
        is_correct = False
    elif isinstance(ground_truth_elems, list):
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

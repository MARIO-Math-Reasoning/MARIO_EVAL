import re 
from typing import Optional

from sympy import simplify, im, N, Equality, Expr
from sympy import re as sympy_re

from .evaluations import is_latex_equiv, is_equiv, is_equiv_possible_matrix, is_equiv_possible_tuple
from .latex_normalize import (
    string_normalize,
    _str_to_complex,
    split_tuple, 
    split_matrix,
    _is_frac, 
    _str_is_int,
    _str_is_mat,
    _str_to_mat,
    _str_to_interval,
)
from .latex_parser import latex2sympy_wrapper, are_equal_under_sympy, _are_equal_latex_sympy
from .constants import *


def is_equiv_complex(
    ground_truth: str, 
    prediction: str,
    verbose: bool = False,
)-> bool:
    ground_truth = _str_to_complex(ground_truth)
    prediction = _str_to_complex(prediction)

    grt_normalized = string_normalize(ground_truth, lower_case=False).replace("\\sqrt{-1}", "I")
    pre_normalized = string_normalize(prediction, lower_case=False).replace("\\sqrt{-1}", "I")

    try:
        if isinstance(grt_normalized, set) or isinstance(pre_normalized, set):
            if isinstance(grt_normalized, str):
                grt_normalized = {grt_normalized}
            if isinstance(pre_normalized, str):
                pre_normalized = {pre_normalized}
            for grt_norm in grt_normalized:
                for pre_norm in pre_normalized:
                    try:
                        if is_latex_equiv(grt_norm, pre_norm, verbose=verbose):
                            return True
                    except:
                        continue
            return False
        else:
            return is_latex_equiv(grt_normalized, pre_normalized, verbose=verbose)
    except:
        return False


def try_to_parse_function(expr: str):
    idx = expr.find("=") 
    if idx > 0:
        lhs_str = expr[:idx]
        rhs_str = expr[idx + 1:]
        try:
            f_lhs = latex2sympy_wrapper(lhs_str)
            inv_f_lhs = 1 / f_lhs
            # if (f_lhs.is_Function and getattr(f_lhs, "name", None)) \
            #     or (inv_f_lhs.is_Function and getattr(inv_f_lhs, "name", None)) \
            #         or f_lhs.is_symbol:
            #     print(f"{lhs_str}={rhs_str} may not be a function?") 
            return rhs_str
        except:
            pass
    return expr


def is_equiv_function(
    ground_truth: str, 
    prediction: str, 
    verbose: bool = False,
) -> bool:
    """
    For function, in the following forms: f(x) =, z =, g^-1(x) = , y = ,
        we take the right side
    If no "=", we directly take the expression itself.
    """
    if is_equiv(ground_truth, prediction):
        return True
    
    grt_normalized = string_normalize(ground_truth)
    pre_normalized = string_normalize(prediction)
    
    grt_func = try_to_parse_function(grt_normalized)
    pre_func = try_to_parse_function(pre_normalized)

    return is_equiv(grt_func, pre_func)


def is_equiv_vector(
    ground_truth: str,
    prediction: str,
    verbose: bool = False,
) -> bool:
    grt_normalized = string_normalize(ground_truth)
    pre_normalized = string_normalize(prediction)

    def preprocess(normalized: str) -> str:
        if (normalized.startswith("(") and normalized.endswith(")")) or (normalized.startswith("[") and normalized.endswith("]")):
            return normalized
        elif normalized.startswith("{") and normalized.endswith("}"):
            normalized = "[" + normalized[1:-1] + "]"
        else:
            normalized = "[" + normalized + "]"
        return normalized

    grt_normalized = preprocess(grt_normalized)
    pre_normalized = preprocess(pre_normalized)
    try:
        is_correct, _ = is_equiv_possible_tuple(grt_normalized, pre_normalized, verbose)
        return is_correct
    except:
        return False


def is_equiv_set(
    ground_truth: str, 
    prediction: str, 
    verbose: bool = False,
) -> bool:
    grt_normalized = string_normalize(ground_truth)
    pre_normalized = string_normalize(prediction)

    def preprocess(normalized: str) -> str:
        if (normalized.startswith("(") and normalized.endswith(")")) or (normalized.startswith("[") and normalized.endswith("]")):
            normalized = normalized[1:-1]
        return normalized

    grt_normalized = preprocess(grt_normalized)
    pre_normalized = preprocess(pre_normalized)
    try:
        is_correct, _ = is_equiv_possible_tuple(grt_normalized, pre_normalized, verbose)
        return is_correct
    except:
        return False


def is_equiv_type(
    ground_truth: str,
    prediction: str, 
    answer_type: Optional[str] = None,
    verbose: bool = False,
) -> bool:
    # Mapping from answer types to their respective checking functions
    equiv_checks = {
        'Complex': is_equiv_complex,
        'Set': is_equiv_set,  
        'Vector': is_equiv_vector,
        'Function': is_equiv_function,
        # 'Real': is_equiv,
        # 'Interval(s)': is_equiv,
        # 'Matrix': is_equiv,
        # 'Expression': is_equiv,
        # 'Equation': is_equiv,  
        # 'Inequality': is_equiv,
        # 'Others': is_equiv,
    }
    is_equal = False
    for type_name, check_func in equiv_checks.items():
        if re.search(type_name, answer_type): 
            if check_func(ground_truth, prediction):
                is_equal = True
                break 
        else:
            continue
    if not is_equal:
        is_equal = is_equiv(ground_truth, prediction, verbose)
    return is_equal
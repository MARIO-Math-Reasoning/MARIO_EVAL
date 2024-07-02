"""match in sympy"""
import random
import re
import sympy

from typing import Tuple, Any, Dict, Optional

from sympy.parsing.latex import parse_latex
from sympy.parsing import sympy_parser
from sympy import Symbol, pi, Expr, Matrix, I
from sympy.core.relational import Equality, Relational
from latex2sympy.latex2sympy2 import latex2sympy
from timeout_decorator import timeout

from .constants import *


BAD_SUBSTRINGS = ["^{", "^("]
BAD_REGEXES = ["\^[0-9]+\^", "\^[0-9][0-9]+"]


def _sympy_parse(expr: str) -> Tuple[Any, Any]:
    """Parses an latex expression with sympy

    if latex2sympy success:
        l2s_expr is sympy expr
    else:
        l2s_expr is str

    if parse_latex success:
        sp_expr is sympy expr
    else:
        sp_expr is str
    
    if parse_expr success:
        sp_or_py_expr is sympy expr or python expr(e.g., [x, y] -> list of sympy expr)
    else:
        sp_or_py_expr is str
    
    """
    try:
        l2s_expr = latex2sympy(expr)
    except:
        l2s_expr = None

    sp_expr = None
    if l2s_expr is None:
        try:
            sp_expr = parse_latex(expr).subs({Symbol('pi'): pi})
        except:
            pass
    
    py_expr = expr.replace("^", "**")
    try:
        sp_or_py_expr = sympy_parser.parse_expr(
            py_expr,
            transformations=(
                sympy_parser.standard_transformations
                + (sympy_parser.implicit_multiplication_application,)
            ),
            # backend='lark'
        )
        if isinstance(sp_or_py_expr, tuple) and len(sp_or_py_expr) > 2:
            # cannot be interval
            sp_or_py_expr = list(sp_or_py_expr)
        # remove duplicated
        if l2s_expr and sp_or_py_expr == l2s_expr:
            sp_or_py_expr = None
        if sp_expr and sp_or_py_expr == sp_expr:
            sp_or_py_expr = None
    except:
        sp_or_py_expr = None

    return [l2s_expr, sp_expr, sp_or_py_expr]


def count_unknown_letters_in_expr(expr: str):
    expr = expr.replace("sqrt", "")
    expr = expr.replace("frac", "")
    letters_in_expr = set([x for x in expr if x.isalpha()])
    return len(letters_in_expr)


def should_allow_eval(expr: str):
    # we don't want to try parsing unknown text or functions of more than two variables
    if count_unknown_letters_in_expr(expr) > 2:
        return False

    for bad_string in BAD_SUBSTRINGS:
        if bad_string in expr:
            return False

    for bad_regex in BAD_REGEXES:
        if re.search(bad_regex, expr) is not None:
            return False

    return True


def _is_sympy_zero(expr) -> bool:
    if isinstance(expr, Expr):
        return expr == 0 or expr.is_zero
    elif isinstance(expr, Matrix):
        return expr.is_zero_matrix
    return False


def _get_sympy_type(latex_sympy: Any) -> str:
    """
    latex_sympy can be sympy expr or str
    """
    if isinstance(latex_sympy, list):
        return ANSWER_TYPE_VEC
    elif isinstance(latex_sympy, set):
        return ANSWER_TYPE_SET
    elif isinstance(latex_sympy, Equality):
        ltx_lhs = latex_sympy.lhs
        inv_ltx_lhs = 1/ltx_lhs
        if (ltx_lhs.is_Function and getattr(ltx_lhs, "name", None)) \
            or (inv_ltx_lhs.is_Function and getattr(inv_ltx_lhs, "name", None)) \
                or ltx_lhs.is_symbol:
            """
            f(x) = , g(x) =, f^{-1}(x) = , y = , z =, ...
            """
            return ANSWER_TYPE_FUNC
        else:
            return ANSWER_TYPE_EQUL
    elif isinstance(latex_sympy, Relational) and latex_sympy.rel_op != "==":
        # Equality is also Relational, so we decide it in first. 
        # Note: `Unequality`.rel_op is "!="
        return ANSWER_TYPE_INEQ
    elif isinstance(latex_sympy, Expr):
        if latex_sympy.has(sympy.I):
            return ANSWER_TYPE_CPLX
        else:
            return ANSWER_TYPE_EXPR
    elif isinstance(latex_sympy, Matrix):
        return ANSWER_TYPE_MAT
    else:
        return ANSWER_TYPE_OTHS


def _list_to_mat(list_expr, exp_rows, exp_cols):
    mat = Matrix(list_expr)
    if mat.rows == exp_rows and mat.cols == exp_cols:
        return mat
    elif (exp_rows == 1 and mat.rows == exp_cols) or (exp_cols == 1 and mat.cols == exp_rows):
        # row and col vector are equvilent
        return mat.transpose()
    else:
        raise ValueError("Matrix dimension does not match.")


def _ineq_to_expr(ineq):
    if ineq.rel_op in {"<=", "<"}:
        return ineq.lhs - ineq.rhs
    elif ineq.rel_op in {">=", ">"}:
        return ineq.rhs - ineq.lhs
    else:
        raise ValueError(f"The {ineq} is not Inequality.")


def _uneq_to_set(uneq):
    if uneq.rel_op == "!=":
        return {uneq.lhs, uneq.rhs}
    else:
        raise ValueError(f"The {uneq} is not Unequality.")


def expr_with_only_i(latex_sympy):
    # If the expression has only one var "i", replace it with sympy.I
    is_cplx = False
    if len(latex_sympy.free_symbols) == 1:
        unknown_var = latex_sympy.free_symbols.pop()
        if unknown_var.name == "i":
            latex_sympy = latex_sympy.subs(unknown_var, I)
            is_cplx = True
    return latex_sympy, is_cplx


def sympy_simplify(sympy_expr: Expr):

    @timeout(TIMEOUT_SECONDS, exception_message=TIMEOUT_MESSAGE.format(func_name="sympy_simplify", seconds=TIMEOUT_SECONDS))
    def _sympy_simplify(sympy_expr):
        if sympy_expr.is_number:
            return sympy_expr.evalf()
        return sympy.simplify(sympy_expr)
    
    try:
        return _sympy_simplify(sympy_expr)
    except Exception as e:
        print(("{}: {}".format(type(e).__name__, str(e))))
        raise RuntimeError


def sympy_expand_equal(gt_sympy_expr: Expr, gv_sympy_expr: Expr) -> bool:

    @timeout(TIMEOUT_SECONDS, exception_message=TIMEOUT_MESSAGE.format(func_name="sympy_expand_equal", seconds=TIMEOUT_SECONDS))
    def _sympy_expand_equal(gt_sympy_expr, gv_sympy_expr):
        return bool(gt_sympy_expr.expand(trig=True) == gv_sympy_expr.expand(trig=True))
    
    try:
        return _sympy_expand_equal(gt_sympy_expr, gv_sympy_expr)
    except Exception as e:
        print(("{}: {}".format(type(e).__name__, str(e))))
        return False


def sympy_abs(sympy_expr: Expr):

    @timeout(TIMEOUT_SECONDS, exception_message=TIMEOUT_MESSAGE.format(func_name="sympy_abs", seconds=TIMEOUT_SECONDS))
    def _sympy_abs(sympy_expr):
        # return sympy.Abs(sympy_expr)
        return abs(sympy_expr) 
    
    try:
        return _sympy_abs(sympy_expr)
    except Exception as e:
        print(("{}: {}".format(type(e).__name__, str(e))))
        raise RuntimeError


def sympy_evalf(
    sympy_expr: Expr, 
    symbols_: Optional[Dict[Symbol, float]] = None,
) -> Optional[float]:

    @timeout(TIMEOUT_SECONDS, exception_message=TIMEOUT_MESSAGE.format(func_name="sympy_evalf", seconds=TIMEOUT_SECONDS))
    def _sympy_evalf(sympy_expr, symbols_=None):
        return sympy_expr.evalf(subs=symbols_)
        
    try:
        return _sympy_evalf(sympy_expr, symbols_)
    except Exception as e:
        print(("{}: {}".format(type(e).__name__, str(e))))
        return None


def _numerical_equal(
    gt_latex_sympy,
    gv_latex_sympy,
    rng,
) -> bool:
    if not gt_latex_sympy.free_symbols == gv_latex_sympy.free_symbols:
        return False
    
    gt_symbols = list(gt_latex_sympy.free_symbols)
    flag = True
    for _ in range(10):
        symbols_ = {a: rng(1, 10) for a in gt_symbols}
        temp_gt = sympy_evalf(gt_latex_sympy, symbols_)
        temp_gv = sympy_evalf(gv_latex_sympy, symbols_)
        if temp_gt is None or temp_gv is None or not _diff_equal(temp_gt, temp_gt - temp_gv):
            flag = False
            break
    return flag


def _diff_equal(
    gt_latex_sympy,
    diff_latex_sympy,
) -> bool:
    if _is_sympy_zero(diff_latex_sympy):
        return True

    def abs_smaller_than_threshold(latex_sympy, threshold: float) -> bool:
        try:
            abs_latex_sympy = sympy_abs(latex_sympy)
            return abs_latex_sympy < threshold or sympy_evalf(abs_latex_sympy) < threshold
        except:
            return False

    diff_equal = False
    if diff_latex_sympy.is_number:
        if gt_latex_sympy.free_symbols or gt_latex_sympy.is_Integer:
            # TODO: should check coeff of var in diff_latex_sympy.free_symbols < EPSILON
            diff_equal = abs_smaller_than_threshold(diff_latex_sympy, EPSILON)
        elif sympy_abs(gt_latex_sympy) >= 1:
            diff_equal = abs_smaller_than_threshold(diff_latex_sympy, 5 * EPSILON)
        elif gt_latex_sympy.is_number and sympy_abs(gt_latex_sympy) > 0:
            diff_equal = abs_smaller_than_threshold(diff_latex_sympy / gt_latex_sympy, EPSILON)

    return diff_equal


def _are_equal_latex_sympy(
    gt_latex_sympy: Any, 
    gv_latex_sympy: Any,
    gt_type: str,
    gv_type: str,
) -> bool:
    if gt_type in {ANSWER_TYPE_VEC, ANSWER_TYPE_SET} and gv_type in {ANSWER_TYPE_VEC, ANSWER_TYPE_SET} and gt_type != gv_type:
        return False

    if gt_type == gv_type == ANSWER_TYPE_VEC:
        if len(gt_latex_sympy) != len(gv_latex_sympy):
            return False
        
        for _gt, _gv in zip(gt_latex_sympy, gv_latex_sympy):
            _gt_type = _get_sympy_type(_gt)
            _gv_type = _get_sympy_type(_gv)
            if not _are_equal_latex_sympy(_gt, _gv, _gt_type, _gv_type):
                return False
        
        return True

    if gt_type == gv_type == ANSWER_TYPE_SET:
        if len(gt_latex_sympy) != len(gv_latex_sympy):
            return False
        
        for i, _gt in enumerate(gt_latex_sympy):
            _gt_type = _get_sympy_type(_gt)
            found_match = False
            for _gv in gv_latex_sympy:
                _gv_type = _get_sympy_type(_gv)
                if _are_equal_latex_sympy(_gt, _gv, _gt_type, _gv_type):
                    found_match = True
                    break
            if not found_match:
                return False
        
        return True
    
    if gt_type == gv_type == ANSWER_TYPE_EQUL:
        gt_latex_sympy = gt_latex_sympy.lhs - gt_latex_sympy.rhs
        gv_latex_sympy = gv_latex_sympy.lhs - gv_latex_sympy.rhs
        gt_type = _get_sympy_type(gt_latex_sympy)
        gv_type = _get_sympy_type(gv_latex_sympy)
        return _are_equal_latex_sympy(gt_latex_sympy, gv_latex_sympy, gt_type, gv_type) \
            or _are_equal_latex_sympy(-gt_latex_sympy, gv_latex_sympy, gt_type, gv_type) 

    if gt_type == gv_type == ANSWER_TYPE_INEQ:
        if (gt_latex_sympy.rel_op in {"<=", ">="} and gv_latex_sympy.rel_op in {"<=", ">="}) \
            or (gt_latex_sympy.rel_op in {"<", ">"} and gv_latex_sympy.rel_op in {"<", ">"}):
            gt_latex_sympy = _ineq_to_expr(gt_latex_sympy)
            gv_latex_sympy = _ineq_to_expr(gv_latex_sympy)
            gt_type = _get_sympy_type(gt_latex_sympy)
            gv_type = _get_sympy_type(gv_latex_sympy)
            return _are_equal_latex_sympy(gt_latex_sympy, gv_latex_sympy, gt_type, gv_type)
        else:
            # must be `Unequality` with rel_op !=
            # A != B, A1 != B1, we compare two sets: {A, B} and {A1, B1}
            gt_latex_sympy = _uneq_to_set(gt_latex_sympy)
            gt_latex_sympy = _uneq_to_set(gt_latex_sympy)
            gt_type = _get_sympy_type(gt_latex_sympy)
            gv_type = _get_sympy_type(gv_latex_sympy)
            return _are_equal_latex_sympy(gt_latex_sympy, gv_latex_sympy, gt_type, gv_type)

    if gt_type == gv_type == ANSWER_TYPE_MAT:
        gt_rows = gt_latex_sympy.rows
        gt_cols = gt_latex_sympy.cols
        if gv_latex_sympy.rows != gt_rows or gv_latex_sympy.cols != gt_cols:
            return False
        for i in range(gt_rows):
            for j in range(gt_cols):
                gt_elem = gt_latex_sympy[i, j]
                gv_elem = gv_latex_sympy[i, j]
                gt_elem_type = _get_sympy_type(gt_elem)
                gv_elem_type = _get_sympy_type(gv_elem)
                if not _are_equal_latex_sympy(gt_elem, gv_elem, gt_elem_type, gv_elem_type):
                    return False
        return True
    
    if gt_type == ANSWER_TYPE_MAT or gv_type == ANSWER_TYPE_MAT:
        if gv_type == ANSWER_TYPE_VEC:
            gt_rows = gt_latex_sympy.rows
            gt_cols = gt_latex_sympy.cols
            try:
                gv_latex_sympy = _list_to_mat(gv_latex_sympy, gt_rows, gt_cols)
                return _are_equal_latex_sympy(gt_latex_sympy, gv_latex_sympy, gt_type, gt_type)
            except:
                return False
        if gt_type == ANSWER_TYPE_VEC:
            gv_rows = gv_latex_sympy.rows
            gv_cols = gv_latex_sympy.cols
            try:
                gt_latex_sympy = _list_to_mat(gt_latex_sympy, gv_rows, gv_cols)
                return _are_equal_latex_sympy(gt_latex_sympy, gv_latex_sympy, gv_type, gv_type)
            except:
                return False

    if gt_type == gv_type == ANSWER_TYPE_CPLX:
        gt_re = sympy.re(gt_latex_sympy)
        gt_im = sympy.im(gt_latex_sympy)
        gv_re = sympy.re(gv_latex_sympy)
        gv_im = sympy.im(gv_latex_sympy)
        gt_re_type = _get_sympy_type(gt_re)
        gt_im_type = _get_sympy_type(gt_im)
        gv_re_type = _get_sympy_type(gv_re)
        gv_im_type = _get_sympy_type(gv_im)
        return _are_equal_latex_sympy(gt_re, gv_re, gt_re_type, gv_re_type) \
            and _are_equal_latex_sympy(gt_im, gv_im, gt_im_type, gv_im_type)

    if gt_type == gv_type == ANSWER_TYPE_EXPR:
        gt_latex_sympy, gt_is_cplx = expr_with_only_i(gt_latex_sympy)
        gv_latex_sympy, gv_is_cplx = expr_with_only_i(gv_latex_sympy)
        if gt_is_cplx or gv_is_cplx:
            return _are_equal_latex_sympy(gt_latex_sympy, gv_latex_sympy, ANSWER_TYPE_CPLX, ANSWER_TYPE_CPLX)
    
    if gt_type == ANSWER_TYPE_FUNC or gv_type == ANSWER_TYPE_FUNC:
        if isinstance(gt_latex_sympy, Equality):
            gt_latex_sympy = gt_latex_sympy.rhs
            gt_type = _get_sympy_type(gt_latex_sympy)
        if isinstance(gv_latex_sympy, Equality):
            gv_latex_sympy = gv_latex_sympy.rhs
            gv_type = _get_sympy_type(gv_latex_sympy)
        return _are_equal_latex_sympy(gt_latex_sympy, gv_latex_sympy, gt_type, gv_type)

    if gt_latex_sympy.is_number:
        gt_latex_sympy = sympy_evalf(gt_latex_sympy)
    if gv_latex_sympy.is_number:
        gv_latex_sympy = sympy_evalf(gv_latex_sympy)

    # expand
    ltx_ltx_equal = False
    try:
        ltx_ltx_equal = sympy_expand_equal(gt_latex_sympy, gv_latex_sympy)
    except:
        pass

    if ltx_ltx_equal:
        return True

    # simplify
    diff_equal = False
    try:
        diff_latex_sympy = sympy_simplify(gt_latex_sympy - gv_latex_sympy)
        diff_equal = _diff_equal(gt_latex_sympy, diff_latex_sympy)
    except:
        pass

    if diff_equal:
        return True

    # numerical methods
    # sympy.simplify won't further simplify sqrt(f(x)) * sqrt(1/f(x))
    #
    #   e.g., sqrt(x) * sqrt(1/x) is the final simplest form, unless define x = symbols("x", positive=True)
    #       if x > 0, sqrt(x) * sqrt(1/x) = 1
    #       if x < 0, sqrt(x) * sqrt(1/x) = -1
    try:
        if gt_latex_sympy.free_symbols and gv_latex_sympy.free_symbols:
            # integer
            num_equal = _numerical_equal(gt_latex_sympy, gv_latex_sympy, random.randint)
            if not num_equal:
                # float 
                num_equal = _numerical_equal(gt_latex_sympy, gv_latex_sympy, random.uniform)
            return num_equal
    except:
        return False


def are_equal_with_simplify(
    ground_truth_normalized: str, 
    given_normalized: str,
    verbose: bool = False,
) -> bool:
    gt_latex_sympy_candidates = _sympy_parse(ground_truth_normalized)
    gv_latex_sympy_candidates = _sympy_parse(given_normalized)

    if verbose:
        print(gt_latex_sympy_candidates)
        print(gv_latex_sympy_candidates)

    ltx_ltx_equal = False
    for i, gt_latex_sympy in enumerate(gt_latex_sympy_candidates):
        if gt_latex_sympy is None:
            continue
        for j, gv_latex_sympy in enumerate(gv_latex_sympy_candidates):
            if gv_latex_sympy is None:
                continue
            gt_type = _get_sympy_type(gt_latex_sympy)
            gv_type = _get_sympy_type(gv_latex_sympy)
            ltx_ltx_equal = _are_equal_latex_sympy(
                gt_latex_sympy,
                gv_latex_sympy,
                gt_type,
                gv_type,
            )
            if ltx_ltx_equal:
                #print(i, j)
                return True
    
    return False


def are_equal_under_sympy(
    ground_truth_normalized: str, 
    given_normalized: str,
    verbose: bool = False,
):
    """
    Example::

        >>> from math_evaluation.core.latex_parser import are_equal_under_sympy
        >>> pairs = [
        ...     ("{x, x - 1}", "{x - 1, x}"),
        ...     ("[x, x - 1]", "[x - 1, x]"),
        ...     ("f(x) = x^2", "y = x^2"),
        ...     ("\\begin{matrix} x \\\\ \\sqrt{3} + 2i  \\\\ \\frac12 \\end{matrix}", "\\begin{matrix} x \\\\ \\sqrt{3} + 2i \\\\ 0.5 \\end{matrix}"),
        ...     ("\\begin{matrix} \\frac12 \\\\ 1 \\end{matrix}", "[0.5, 1]")
        ... ]
        >>> for ans, prd in pairs:
        ...     res = are_equal_under_sympy(ans, prd)
        ...     print(res)
        ... 
        True
        False
        True
        True
        True

    """
    are_equal = False
    try:
        if are_equal_with_simplify(ground_truth_normalized, given_normalized, verbose):
            return True
    except:
        pass

    # try:
    #     expr = f"({ground_truth_normalized})-({given_normalized})"
    #     gt_latex_sympy_candidates = _sympy_parse(ground_truth_normalized)
    #     sympy_diff_candidates = _sympy_parse(expr)
    #     for gt_latex_sympy in gt_latex_sympy_candidates:
    #         if gt_latex_sympy is None:
    #             continue
    #         for sympy_diff in sympy_diff_candidates:
    #             if sympy_diff is None:
    #                 continue
    #             simplified_diff = sympy_simplify(sympy_diff)
    #             if _diff_equal(gt_latex_sympy, simplified_diff):
    #                 are_equal = True
    #                 break
    #         if are_equal:
    #             break
    # except:
    #     pass

    return are_equal

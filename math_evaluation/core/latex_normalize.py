"""string preprocessing"""
import re
import sympy

from typing import Optional
from .latex_parser import latex2sympy_wrapper

from .constants import *


def _parse_latex(expr: str) -> str:
    """Attempts to parse latex to an expression sympy can read."""
    expr = expr.replace("\\tfrac", "\\frac")
    expr = expr.replace("\\cfrac", "\\frac")
    expr = expr.replace("\\dfrac", "\\frac")

    # expr = latex2text.LatexNodes2Text().latex_to_text(expr).replace("\n", "")
    # expr = add_parentheses_after_keyword(expr, [ADD_PARENTHESES_AFTER_KEYWORD[0]], candidate_num=1)
    # expr = expr.replace("ADDED_PARENTHESES_LEFT", "{")
    # expr = expr.replace("ADDED_PARENTHESES_RIGHT", "}")
    # expr = add_parentheses_after_keyword(expr, [ADD_PARENTHESES_AFTER_KEYWORD[1]], candidate_num=2)
    # expr = expr.replace("ADDED_PARENTHESES_LEFT", "{")
    # expr = expr.replace("ADDED_PARENTHESES_RIGHT", "}")
    # Replace the specific characters that this parser uses.

    expr = expr.replace("√", "sqrt")
    expr = expr.replace("π", "pi")
    expr = expr.replace("∞", "inf")
    expr = expr.replace("∪", "U")
    expr = expr.replace("·", "*")
    expr = expr.replace("×", "*")

    return expr.strip()


def _str_to_complex(complex_num: str):
    """change imagenary unit to \\sqrt{-1}

    usually no letters before or after i, e.g., i in `in` `sin`, `begin` are not imagenary unit.
    
    BE CAREFUL to use this function, because
        To infer `i` in the expression, we'd better assume the type must be complex
        So we ONLY use it in `is_equiv_complex`
        A better way is to first ask LLM to capitalize imagenary unit as `I`, then call this function.
    
    Will transform
        Good cases: 1 + 2i, 1 + 2*i, i(1+i), \\sin(x) + \\cos(x)i, x + y i
        Bad cases:  \\sum_{i=1} x^i

    Won't transform
        Good cases: x_i, 
        Bad cases:  x + yi
    """
    if "I" in complex_num:
        return complex_num.replace("I", "\\sqrt{-1}")
    elif "i" in complex_num:
        regex = r"((?<!\w)i(?!\w))|((?<=\s)i(?=\s))|((?<=\s)i(?=\W))|((?<=\W)i(?=\s))|((?<=\W)i(?=\W))|((?<=\d)i)"
        pattern = re.compile(regex)
        return pattern.sub(r"\\sqrt{-1}", complex_num)
    else:
        return complex_num


def _is_float(num: str) -> bool:
    try:
        float(num)
        return True
    except ValueError:
        return False


def _is_int(x: float) -> bool:
    try:
        return abs(x - int(round(x))) <= 1e-7
    except:
        return False


def _is_frac(expr: str) -> bool:
    return ('matrix' not in expr) and (bool(re.search(r"^-?[0-9]+.?/0*[1-9][0-9]*.?$", expr)) or bool(re.search(r"[frac]", expr)))


def _strip_properly_formatted_commas(expr: str):
    expr = re.sub(r"\d{1,3}(?:, ?\d{3})+", lambda x: x.group(0).replace(',', ''), expr)
    return expr


def _str_is_int(x: str) -> bool:
    try:
        x = _strip_properly_formatted_commas(x)
        x = float(x)
        return abs(x - int(round(x))) <= 1e-7
    except:
        return False


def _str_is_mat(x: str) -> bool:
    if 'matrix' in x:
        return True
    else:
        return False


def _str_to_int(x: str):
    try:
        x = latex2sympy_wrapper(x)
    except:
        pass
    return x


def _str_to_mat(x: str):
    return latex2sympy_wrapper(x)


def _str_matrix_normalize(expr: str):
    if "{cases}" in expr:
        expr = expr.replace("{cases}", "{matrix}")
    if "{array}" in expr:
        expr = expr.replace("{array}", "{matrix}")
    if not (not "\\\\begin" in expr and "\\begin" in expr and "matrix" in expr):
        expr = expr.replace("\\\\", "\\")
    return expr


def _str_to_interval(x: str):
    try:
        x = x.split('⋃') if '⋃' in x else x.split('\\cup')
        _interval = sympy.EmptySet
        for idx, or_interval in enumerate(x):
            _or_interval = sympy.EmptySet
            for and_interval in or_interval.split('∩') if '∩' in or_interval else or_interval.split('\\cap'):
                and_interval = and_interval.strip()
                int_start, int_end = and_interval.split(',')
                int_start = latex2sympy_wrapper(int_start.replace('(', '').replace('[', ''))
                int_end = latex2sympy_wrapper(int_end.replace(')', '').replace(']', ''))
                # check validation
                if int_start.is_number:
                    int_start = int_start.evalf()
                    if _is_int(int_start):
                        int_start = sympy.Integer(int_start)
                if int_end.is_number:
                    int_end = int_end.evalf()
                    if _is_int(int_end):
                        int_end = sympy.Integer(int_end)
                if int_start.is_number and int_end.is_number and int_start > int_end:
                    raise Exception('Illegal Interval range')
                # define sympy Interval
                temp_int = sympy.Interval(int_start, int_end, left_open='(' in and_interval, right_open=')' in and_interval)
                if _or_interval.is_empty:
                    _or_interval = temp_int
                else:
                    _or_interval = _or_interval.intersect(temp_int)
            _interval = _interval + _or_interval
        x = _interval
    except:
        return None
    return x


def _inject_implicit_mixed_number(expr: str):
    """
    Automatically make a mixed number evalable

    two cases:
        7 3/4 => 7+3/4: must have space
        7\\frac34 => 7+\\frac34: space is optional
    """
    regex_cands = [
        r"(\d+) +(\d+/\d+)",                    
        r"(\d+) *(\\frac(\d|{\d+})(\d|{\d+}))",  
    ]
    for regex in regex_cands:
        pattern = re.compile(regex)
        expr = pattern.sub(r"\1+\2", expr)
    return expr


def _str_to_decimal(digits: str, base: str):
    tot = 0
    base = int(base)
    for i, d in enumerate(reversed(digits)):
        tot += base ** i * int(d)
    return tot


def _str_to_time_list(expr: str):
    # case 1: am/pm is must, when only hour, 2 am, 2\\text{am}
    regex = r"^(\d{1,2})\s*((?:\\text\{\s*[ap]\.?m\.?\s*\})|(?:[ap]\.?m\.?))$"
    match = re.search(regex, expr, re.IGNORECASE)
    if match:
        hour, meridiem = match.group(1, 2)
        if "p.m." in meridiem.lower() or "pm" in meridiem.lower():
            hour = {
                str(int(hour) % 12),
                str(int(hour) % 12 + 12),
            }
        return hour

    # case 2: am/pm is optional, but : is must, e.g., 20:00, 8:00pm
    regex = r"^(\d{1,2}):(\d{2})(?::(\d{2}))?\s*((?:\\text\{\s*[ap]\.?m\.?\s*\})|(?:[ap]\.?m\.?))?$"
    match = re.search(regex, expr, re.IGNORECASE)
    if match:
        hour, minute, second, meridiem = match.group(1, 2, 3, 4)
        # second and meridem could be None
        if meridiem and ("p.m." in meridiem.lower() or "pm" in meridiem.lower()):  
            hour = [
                str(int(hour) % 12),
                str(int(hour) % 12 + 12),
            ]
        if second and int(second) != 0:
            if isinstance(hour, list):
                return {
                    f"[{hour[0]}, {int(minute)}, {int(second)}]",
                    f"[{hour[1]}, {int(minute)}, {int(second)}]",
                }
            return f"[{int(hour)}, {int(minute)}, {int(second)}]"
        else:
            # only consider hour and minute
            if int(minute) == 0:
                if isinstance(hour, list):
                    return set(hour)
                return str(int(hour))
            else:
                if isinstance(hour, list):
                    return {
                        f"[{hour[0]}, {int(minute)}]",
                        f"[{hour[1]}, {int(minute)}]",
                    }
                return f"[{int(hour)}, {int(minute)}]"

    return expr


def string_normalize(
    expr: str,
    remove_mid_std_space: bool = True,
    lower_case: bool = True,
):
    try:
        return _string_normalize(expr, remove_mid_std_space, lower_case)
    except Exception as e:
        print(("{}: {}".format(type(e).__name__, str(e))))
        return expr


def _string_normalize(
    expr: str,
    remove_mid_std_space: bool,
    lower_case: bool,
):
    if expr is None:
        return None
    
    # remove leading and trailing space
    expr = expr.strip(" ")

    # latex matrix has \\\\ which cannot be replaced, e.g., \\begin{matrix} 1 & 2 \\\\ 3 & 4 \\end{matrix}
    expr = _str_matrix_normalize(expr)

    # Remove enclosing `\\text{}` or `\\mbox`
    m = re.search(r"^\\\s*(text|mbox){\s*(?P<text>.+?)}$", expr, re.DOTALL)
    if m:
        expr = m.group("text")
        return string_normalize(expr, remove_mid_std_space, lower_case)

    # Extract yyy from {xxx | yyy }
    m = re.search(r"^\\{(.*)\|(.*)\\}$", expr, re.DOTALL)
    if m:
        expr = m.group(2) if m.group(2) else m.group(3)
        return string_normalize(expr, remove_mid_std_space, lower_case)

    # Remove all kinds of space
    expr = re.sub(r"\\:", "", expr)
    expr = re.sub(r"\\,", "", expr)
    expr = re.sub(r"\\;", "", expr)
    expr = re.sub(r"\\!", "", expr)

    # "{,}" -> ","
    expr = re.sub(r"\{,\}", ",", expr)

    # Transform non decimal integer
    m = re.search(r"^(\d+)_(?:(\d)|\{(\d+)\})$", expr)
    if m:
        digits = m.group(1)
        base = m.group(2) if m.group(2) else m.group(3)
        # return f"[{digits}, {base}]"
        # sometimes the answer may not have "_base", we adopt the following logic.
        decimal_digits = _str_to_decimal(digits, base)
        return {
            digits,
            str(decimal_digits),
        }

    # Remove \\% and transform to two possible values for ground truth
    # comparable grd v.s. prd: 10% v.s. 10.0%, 10% v.s. 0.1, 10% v.s. 10
    if "%" in expr:
        expr = expr.replace("\\%", "%")
        expr = expr.replace("%", "")
        if _is_float(expr):
            return {
                str(float(expr) / 100), 
                str(float(expr)),
            }

    # Remove $
    expr = expr.replace("\\$", "$")
    expr = expr.replace("$", "")

    # Normalize "or" and "and" to " , "
    regex = r",? *((\\text\{ *(and|or) *\})| (and|or) )"
    expr = re.sub(regex, " , ", expr)

    expr = expr.replace("million", "*10^6")
    expr = expr.replace("billion", "*10^9")
    expr = expr.replace("trillion", "*10^12")

    expr = expr.replace('\f', '\\f')    # \x0c -> \\a    
    expr = expr.replace('\b', '\\b')    # \x08 -> \\b
    expr = expr.replace('\a', '\\a')    # \x07 -> \\a
    expr = expr.replace('\t', '\\t')
    expr = expr.replace('\r', '\\r')    # for \right -> \\right

    # change \\left( or [ -> (, [, and \\right
    expr = re.sub(r"\\left\(", "(", expr)
    expr = re.sub(r"\\left\[", "[", expr)
    expr = re.sub(r"\\right\)", ")", expr)
    expr = re.sub(r"\\right\]", "]", expr)

    # remove x \in
    expr = re.sub(r"[a-zA-Z]+\s*\\in", "", expr)

    # units in \\text{xxx}
    # Special case for time, transform to list, e.g., "08:30 \\text{pm}" -> "[8, 30]"
    expr = _str_to_time_list(expr)
    if isinstance(expr, set):
        return expr

    # remove unit
    # we only deal with valid power,
    #   e.g., \\text{cm}^d, d must be single digit. 
    #         \\text{cm}^10 does not meet latex syntax.
    #         \\text{cm}^{10} is valid.
    for unit in UNIT_LIST:
        regex = r"(\\)+text{{\s*{unit}(es|s)? *(\^\d|\^{{\d+}})?}} *(\^\d|\^{{\d+}})?".format(unit=unit)
        expr = re.sub(regex, "", expr)
        regex = r"(\\)+mbox{{\s*{unit}(es|s)? *(\^\d|\^{{\d+}})?}} *(\^\d|\^{{\d+}})?".format(unit=unit)
        expr = re.sub(regex, "", expr)

    # remove all \\text{xxx} no matter what xxx is?
    regex = r"(\\)+text\{[a-zA-Z ]+(\^\d|\^\{\d+\})? *\} *(\^\d|\^\{\d+\})?"
    expr = re.sub(regex, "", expr)

    # unit without \\text{}
    # For long unit: without text but with space, e.g., 5 cm, 5 cm^2 -> 5
    # MUST have space between value and unit, e.g., 5cm -> 5*c*m
    # single letter unit is not considered, e.g., m in 5 + m or 5 m
    for unit in UNIT_LONG_LIST:
        regex = r" *{unit}(es|s)? *(\^\d|\^{{\d+}}+)?".format(unit=unit)
        expr = re.sub(regex, "", expr)
    # For short unit: 
    #   MUST have space between value and unit, 
    #   e.g., 5 cm, 5 cm^2 -> 5
    #         5cm -> 5*c*m
    for unit in UNIT_SHORT_LIST:
        regex = r" +{unit}(es|s)? *(\^\d|\^{{\d+}}+)?".format(unit=unit)
        expr = re.sub(regex, "", expr)
    # We didn't consider single letter unit without \\text{}.

    # process X^\\circ to X or X/180 * \\pi 
    circ_pattern = r"\^ *(?:\{ *\\circ *\}|\\circ)"
    if re.search(circ_pattern, expr):
        # first answer: just remove circ
        expr1 = re.sub(circ_pattern, "", expr)
        # second second: change xxx^\\circ => xxx / 180 * \\pi
        regex = r"(\d*)(\.\d+)? *\^ *(?:\{ *\\circ *\}|\\circ)"
        pattern = re.compile(regex)
        expr2 = pattern.sub(r"\1\2/180*\\pi", expr)
        return {
            further_string_normalize(expr1, remove_mid_std_space, lower_case),
            further_string_normalize(expr2, remove_mid_std_space, lower_case),
        }

    return further_string_normalize(expr, remove_mid_std_space, lower_case)


def further_string_normalize(
    expr: str, 
    remove_mid_std_space: bool,
    lower_case: bool,
):
    """Normalize str expressions"""
    if len(expr) > 0 and expr[0] == "{" and expr[-1] == "}":
        expr = expr[1:-1]
    
    if _is_float(expr) and _is_int(float(expr)):
        if re.search("e", expr):
            expr = float_to_latex_scientific(expr)
        else:
            expr = str(int(round(float(expr))))

    if "\\" in expr:
        try:
            expr = _parse_latex(expr)
        except:
            pass

    # edge case with mixed numbers and negative signs
    expr = re.sub("- *", "-", expr)

    expr = _inject_implicit_mixed_number(expr)

    if remove_mid_std_space:
        expr = expr.replace(" ", "")

    # don't be case sensitive for text answers
    # TODO: 
    #   1. lowercase will make complex evaluation is not reliable.
    #       "x + \sqrt{2}I" => "x + \sqrt{2}i", i will become an unknown variable.
    #   2. if expression has ONLY one unknown variable "i", it is fine.
    #       In `expr_with_only_i` of latex_parser.py: "1+2i" => 1+2I, "i(2-i)" => I(2-I), so the two are equal.
    if lower_case:
        expr = expr.lower()

    if _str_is_int(expr):
        expr = str(_str_to_int(expr))

    return expr


def float_to_latex_scientific(expr: str) -> str:
    if _is_float(expr):
        num = float(expr)
        if num != 0:
            # float to sci num, x.xxxe+02
            sci_num = '{:e}'.format(num)
            # computable latex, e -> *10
            latex_sci_num = sci_num.replace('e', '*10^{') + '}'
            return latex_sci_num

    return expr


def split_tuple(expr: str, expected_type: Optional[type] = None):
    """
    Split the elements in a tuple/interval, while handling well-formatted commas in large numbers

    Only consider first and last brackets are matched and no bracket between the first and last brackets

    "(x, y, z)" or "[x, y, z]" -> ["x", "y", "z"]
    "x, y, z" or "{x, y, z}" -> {"x", "y", "z"}
    "[(1, 2), (2,3)]" -> ["(1, 2)", "(2,3)"]
    """
    expr = _strip_properly_formatted_commas(expr)

    # check whether to remove parenthesis
    # (1, 2), (3, 4) should not be tuple
    cnt = 0
    n = len(expr)
    remove_parenthesis = True
    for i, ch in enumerate(expr):
        cnt += (ch == "[" or ch == "(" or ch == "{")
        cnt -= (ch == "]" or ch == ")" or ch == "}")
        if cnt == 0 and i < n - 1:
            remove_parenthesis = False

    assert cnt == 0, "parenthesis not match"

    return_type = set
    if remove_parenthesis and len(expr) > 2:
        if expr[0] + expr[-1] == "[]":
            expr = expr[1:-1]
            return_type = list
        elif expr[0] + expr[-1] == "()":
            expr = expr[1:-1]
            return_type = tuple
        elif expr[0] + expr[-1] == "{}":
            expr = expr[1:-1]
            return_type = set
    
    if expected_type:
        return_type = expected_type
    
    cnt = 0
    stack = []
    result = []
    for ch in expr:
        if ch == "," and cnt == 0:
            result.append("".join(stack).strip())
            stack = []
        else:
            stack.append(ch)
            cnt += (ch == "[" or ch == "(" or ch == "{")
            cnt -= (ch == "]" or ch == ")" or ch == "}")
    
    if stack:
        result.append("".join(stack).strip())
    
    if len(result) > 1:
        return return_type(result)
    else:
        return expr


def split_matrix(expr: str):
    """
    Since SymPy version 1.9.

    non-Expr objects in a Matrix is deprecated. Matrix represents
    a mathematical matrix. To represent a container of non-numeric
    entities, Use a list of lists, TableForm, NumPy array, or some
    other data structure instead.

    See https://docs.sympy.org/latest/explanation/active-deprecations.html#deprecated-non-expr-in-matrix
    for details.

    This function will transform matrix string into list of string list. 
    We consider row vector and column vector are equivalent.

    e.g., 
    row vector: "\\begin{matrix} a & b & c \\end{matrix}"           -> ["a", "b", "c"]
    col vector: "\\begin{matrix} a \\\\ b \\\\ c \\end{matrix}"     -> ["a", "b", "c"]
    matrix:     "\\begin{matrix} a & b \\\\ c & d \\end{matrix}"    -> [["a", "b"], ["c", "d"]]

    row vector: "[a, b, c]"                                         -> ["a", "b", "c"]
    col vector: "[[a], [b], [c]]"                                   -> ["a", "b", "c"]
    matrix:     "[[a, b], [c, d]]"                                  -> [["a", "b"], ["c", "d"]]
    """
    def check_dim(elements):
        is_matrix = True
        n_col = None
        for col in elements:
            cur_n_col = 1 if isinstance(col, str) else len(col)
            if n_col and cur_n_col != n_col:
                is_matrix = False
                break
            n_col = cur_n_col
            
        if not is_matrix:
            print("WARNING: mismatched dimensions. Won't parse.")
        return is_matrix

    regex = r"^\\begin\{[a-zA-Z]?matrix\}(.*?)\\end\{[a-zA-Z]?matrix\}$"
    match = re.search(regex, expr, re.DOTALL)
    elements = []
    if match:
        rows = match.group(1).split("\\\\")
        for row in rows:
            col = row.split("&")
            if len(col) == 1:
                elements.append(col[0])
            else:
                elements.append(col)

    else:
        is_matrix = True
        rows = split_tuple(expr, list)
        if isinstance(rows, str):
            rows = [rows]
        elements = []
        for row in rows:
            col = split_tuple(row, list)
            elements.append(col)
            
    if elements:
        if len(elements) == 1:
            elements = elements[0]
        if check_dim(elements):
            expr = elements 

    return expr


####################
# Unused functions #
####################
def add_parentheses_after_keyword(latex_str, keywords, candidate_num=1):
    keyword_pattern = '|'.join(re.escape(keyword) for keyword in keywords)
    regex_pattern = r'({})\s*'.format(keyword_pattern) + r'([\s\d])' * candidate_num
    def replacement(match):
        groups = match.groups()
        ret = groups[0]
        for group in groups[1:]:
            ret += 'ADDED_PARENTHESES_LEFT{}ADDED_PARENTHESES_RIGHT'.format(group)
        return ret

    if candidate_num > 1:
        spans = re.finditer(keyword_pattern, latex_str)
        pos = -1
        last_span = None
        paraenthesis_added_num = 0
        for span in spans:
            span = span.span()
            if pos == -1:
                pos = 0
            if last_span is None:
                last_span = span
                continue
            if pos <= last_span[-1] + paraenthesis_added_num:
                pos = last_span[-1] + paraenthesis_added_num
                L_P = 0
                P_flag = False
                pass_first_cand = -1
                first_met = True
                while pos < len(latex_str):
                    if latex_str[pos] == ' ':
                        pos += 1
                        continue
                    if not P_flag and L_P == 0 and latex_str[pos] != '{' and first_met:
                        latex_str = latex_str[:pos] + '{' + latex_str[pos] + '}' + latex_str[pos + 1:]
                        pos += 3
                        pass_first_cand = pos - 1
                        paraenthesis_added_num += 2
                        P_flag = False
                        first_met = False
                        continue

                    if P_flag and L_P == 0 and latex_str[pos] != '{':
                        if pass_first_cand == -1:
                            P_flag = False
                            temp_pre_len = len(latex_str)
                            latex_str = latex_str[:last_span[-1] + paraenthesis_added_num] + add_parentheses_after_keyword(latex_str[last_span[-1] + paraenthesis_added_num: pos - 1], keywords, candidate_num=2) + latex_str[pos - 1:]
                            latex_str = latex_str.replace("ADDED_PARENTHESES_LEFT", "{")
                            latex_str = latex_str.replace("ADDED_PARENTHESES_RIGHT", "}")
                            pos += len(latex_str) - temp_pre_len
                            paraenthesis_added_num += len(latex_str) - temp_pre_len
                            pass_first_cand = pos - 1
                        else:
                            # latex_str = latex_str[: pos] + re.sub(r'([\s\d])', _replacement, latex_str[pos: span[0]]) + latex_str[span[0]:]
                            pos = span[-1] + paraenthesis_added_num
                            break
                    if latex_str[pos] == '{':
                        L_P += 1
                        P_flag = True
                        first_met = False
                    elif latex_str[pos] == '}':
                        L_P -= 1
                        P_flag = True
                        first_met = False
                    pos += 1
                if pass_first_cand == -1:
                    latex_str = latex_str[:last_span[0] + paraenthesis_added_num] + re.sub(regex_pattern, replacement, latex_str[last_span[0] + paraenthesis_added_num: span[0] + paraenthesis_added_num]) + latex_str[span[0] + paraenthesis_added_num:]
                    paraenthesis_added_num += 2 * len(re.findall(regex_pattern, latex_str[last_span[0] + paraenthesis_added_num: span[0] + paraenthesis_added_num]))
                    pos += 2 * len(re.findall(regex_pattern, latex_str[last_span[0] + paraenthesis_added_num: span[0] + paraenthesis_added_num]))
                elif not pass_first_cand == -1:
                    need_add = re.match(r'\s*([\da-z])', latex_str[pass_first_cand + 1:])
                    if need_add is not None:
                        need_add_span = need_add.span()[-1]
                        need_add = need_add[0]
                        if '{' not in latex_str[pass_first_cand: pass_first_cand + need_add_span]:
                            latex_str = latex_str[: pass_first_cand] + latex_str[pass_first_cand :].replace(f'{need_add}', "{" + need_add + "}", 1)
                            paraenthesis_added_num += 2
                            pos += 2
            last_span = span
        if pos <= len(latex_str) and pos != -1:
            spans = re.finditer(keyword_pattern, latex_str)
            for span in spans:
                last_span = span.span()
            pos = last_span[-1]
            L_P = 0
            P_flag = False
            pass_first_cand = -1
            first_met = True
            while pos < len(latex_str):
                if latex_str[pos] == ' ':
                    pos += 1
                    continue
                if not P_flag and L_P == 0 and latex_str[pos] != '{' and first_met:
                    latex_str = latex_str[:pos] + '{' + latex_str[pos] + '}' + latex_str[pos + 1:]
                    pos += 3
                    pass_first_cand = pos - 1
                    paraenthesis_added_num += 2
                    P_flag = False
                    first_met = False
                    continue

                if P_flag and L_P == 0 and latex_str[pos] != '{':
                    if not pass_first_cand:
                        P_flag = False
                        temp_pre_len = len(latex_str)
                        latex_str = latex_str[:last_span[-1] + paraenthesis_added_num] + add_parentheses_after_keyword(latex_str[last_span[-1] + paraenthesis_added_num: pos], keywords, candidate_num=2) + latex_str[pos:]
                        pos += len(re.findall("ADDED_PARENTHESES_LEFT", latex_str)) + len(re.findall("ADDED_PARENTHESES_RIGHT", latex_str))
                        paraenthesis_added_num += len(re.findall("ADDED_PARENTHESES_LEFT", latex_str)) + len(re.findall("ADDED_PARENTHESES_RIGHT", latex_str))
                        latex_str = latex_str.replace("ADDED_PARENTHESES_LEFT", "{")
                        latex_str = latex_str.replace("ADDED_PARENTHESES_RIGHT", "}")
                        pos += len(latex_str) - temp_pre_len
                        paraenthesis_added_num += len(latex_str) - temp_pre_len
                        pass_first_cand = pos - 1
                    else:
                        # latex_str = latex_str[: pos] + re.sub(r'([\s\d])', _replacement, latex_str[pos: ])
                        break
                if latex_str[pos] == '{':
                    L_P += 1
                    P_flag = True
                elif latex_str[pos] == '}':
                    L_P -= 1
                    P_flag = True
                    first_met = False
                pos += 1
            if pass_first_cand == -1:
                latex_str = latex_str[:last_span[0] + paraenthesis_added_num] + re.sub(regex_pattern, replacement, latex_str[last_span[0] + paraenthesis_added_num:])
            elif not pass_first_cand == -1:
                need_add = re.match(r'\s*([\da-z])', latex_str[pass_first_cand + 1:])
                if need_add is not None:
                    need_add_span = need_add.span()[-1]
                    need_add = need_add[0].strip()
                    if '{' not in latex_str[pass_first_cand: pass_first_cand + need_add_span]:
                        latex_str = latex_str[: pass_first_cand] + latex_str[pass_first_cand :].replace(f'{need_add}', "{" + need_add + "}", 1)
                        paraenthesis_added_num += 2
                        pos += 2
        return latex_str
    # if len(re.findall(r'({})\s*'.format(keyword_pattern) + r'{([\s\da-z_\+\-\*\/\^\!\(\)\[\]]+)}' * candidate_num, latex_str)) == len(re.findall(r'({})\s*'.format(keyword_pattern), latex_str)):
    #     return latex_str
    # keyword_pattern_with_paren = '|'.join(re.escape(keyword + '{') for keyword in keywords)
    # if len(re.findall(r'({})\s*'.format(keyword_pattern), latex_str)) == len(re.findall(r'({})\s*'.format(keyword_pattern_with_paren), latex_str)):
    #     return latex_str
    # regex_pattern = r'({})\s*'.format(keyword_pattern) + r'{?([\s\da-z_\+\-\*\/\^\!\(\)\[\]])}?' * candidate_num
    modified_latex_str = re.sub(regex_pattern, replacement, latex_str)
    return modified_latex_str

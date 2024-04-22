"""string preprocessing"""
import re
import sympy

from typing import Optional
#from pylatexenc import latex2text
from latex2sympy.latex2sympy2 import latex2sympy

from .constants import *


def _parse_latex(expr: str) -> str:
    """Attempts to parse latex to an expression sympy can read."""
    expr = expr.replace("\frac", "\\frac")
    expr = expr.replace("\\tfrac", "\\frac")
    expr = expr.replace("\\cfrac", "\\frac")
    expr = expr.replace("\\dfrac", "\\frac")
    expr = expr.replace("\\\\frac", " \\frac")  # Play nice with mixed numbers.

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


# def _is_frac(expr: str) -> bool:
#     return bool(re.search(r"^-?[0-9]+.?/0*[1-9][0-9]*.?$", expr))


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
        x = latex2sympy(x)
    except:
        pass
    return x


def _str_to_mat(x: str):
    return latex2sympy(x)


def _str_to_list(x: str):
    try:
        x = eval(x)
    except:
        pass
    return x


def _str_to_interval(x: str):
    try:
        x = x.split('⋃') if '⋃' in x else x.split('\\cup')
        _interval = sympy.EmptySet
        for or_interval in x:
            _or_interval = sympy.EmptySet
            for and_interval in or_interval.split('∩') if '∩' in or_interval else or_interval.split('\\cap'):
                and_interval = and_interval.strip()
                int_start, int_end = and_interval.split(',')
                int_start = latex2sympy(int_start.replace('(', '').replace('[', ''))
                int_end = latex2sympy(int_end.replace(')', '').replace(']', ''))
                if int_start > int_end:
                    raise Exception('Illegal Interval range')
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


def _strip_properly_formatted_commas(expr: str):
    # We want to be careful because we don't want to strip tuple commas
    regex = r"(\d)(,)(\d\d\d)($|\D)"
    p1 = re.compile(regex)
    while True:
        # \1 = \d       keep
        # \2 = ,        remove
        # \3 = \d\d\d   keep
        # \4 = $|\D     keep
        next_expr = p1.sub(r"\1\3\4", expr)
        if next_expr == expr:
            break
        expr = next_expr
    return next_expr


def string_normalize(expr: str, is_ground_truth: bool = False):
    if expr is None:
        return None
    
    # remove leading and trailing space
    expr = expr.strip(" ")

    # latex matrix has \\\\ which cannot be replaced, e.g., \\begin{matrix} 1 & 2 \\\\ 3 & 4 \\end{matrix}
    if "{cases}" in expr:
        expr = expr.replace("{cases}", "{matrix}")
    if "{array}" in expr:
        expr = expr.replace("{array}", "{matrix}")
    if not (not "\\\\begin" in expr and "\\begin" in expr and "matrix" in expr):
        expr = expr.replace("\\\\", "\\")

    # Remove enclosing `\text{}`.
    m = re.search(r"^\\\s*text{\s*(?P<text>.+?)}$", expr)
    if m:
        expr = m.group("text")
        return string_normalize(expr)

    # Extract yyy from {xxx | yyy }
    m = re.search(r"^\\{(.*)\|(.*)\\}$", expr)
    if m:
        expr = m.group(2) if m.group(2) else m.group(3)
        return string_normalize(expr)

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
        if is_group_truth:
            decimal_digits = _str_to_decimal(digits, base)
            return {
                digits,
                str(decimal_digits),
            }
        else:
            return digits

    # Remove \\% and transform to two possible values for ground truth
    # comparable grd v.s. prd: 10% v.s. 10.0%, 10% v.s. 0.1, 10% v.s. 10
    if "%" in expr:
        expr = expr.replace("\\%", "%")
        expr = expr.replace("%", "")
        if _is_float(expr) and is_ground_truth:
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
        if is_ground_truth:
            # first answer: just remove circ
            expr1 = re.sub(circ_pattern, "", expr)
            # second second: change xxx^\\circ => xxx / 180 * \\pi
            regex = r"(\d*)(\.\d+)? *\^ *(?:\{ *\\circ *\}|\\circ)"
            pattern = re.compile(regex)
            expr2 = pattern.sub(r"\1\2/180*\\pi", expr)
            return {
                further_string_normalize(expr1),
                further_string_normalize(expr2),
            }
        else:
            expr = re.sub(circ_pattern, "", expr)

    return further_string_normalize(expr)


def further_string_normalize(expr: str):
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

    expr = expr.replace(" ", "")

    # don't be case sensitive for text answers
    # TODO: 
    #   1. lowercase will make complex evaluation is not reliable.
    #       "x + \sqrt{2}I" => "x + \sqrt{2}i", i will become an unknown variable.
    #   2. if expression has ONLY one unknown variable "i", it is fine.
    #       In `expr_with_only_i` of latex_parser.py: "1+2i" => 1+2I, "i(2-i)" => I(2-I), so the two are equal.
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


def split_tuple(expr: str, expect_type: Optional[type] = None):
    """
    Split the elements in a tuple/interval, while handling well-formatted commas in large numbers

    Only consider first and last brackets are matched and no bracket between the first and last brackets

    "(x, y, z)" or "[x, y, z]" -> ["x", "y", "z"]
    "x, y, z" -> {x, y, z}
    "[(1, 2), (2,3)]" -> ["(1, 2)", "(2,3)"]
    """
    expr = _strip_properly_formatted_commas(expr)

    return_list = False
    if len(expr) > 2 and expr[0] + expr[-1] in {"[]", "()"}:
        expr = expr[1:-1]
        return_list = True
    
    cnt = 0
    stack = []
    result = []
    for ch in expr:
        if ch == "," and cnt == 0:
            result.append("".join(stack).strip())
            stack = []
        else:
            stack.append(ch)
            cnt += (ch == "[" or ch == "(")
            cnt -= (ch == "]" or ch == ")")
    
    assert cnt == 0, "parenthesis not match"
    if stack:
        result.append("".join(stack).strip())
    
    if len(result) > 1:
        return result if return_list else set(result)
    else:
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

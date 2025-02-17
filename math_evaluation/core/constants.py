TIMEOUT_SECONDS = 15
TIMEOUT_MESSAGE = "Execution of function `{func_name}` has timed out for exceeding {seconds} seconds."

ANSWER_TYPE_CPLX = "complex"
ANSWER_TYPE_VEC = "vector"
ANSWER_TYPE_SET = "set"
ANSWER_TYPE_MAT = "matrix"
ANSWER_TYPE_FUNC = "function"
ANSWER_TYPE_EQUL = "equation"
ANSWER_TYPE_EXPR = "expression"
ANSWER_TYPE_INEQ = "inequality"
ANSWER_TYPE_OTHS = "others"

TUPLE_CHARS = "()[]"

EPSILON = 1e-3

INVALID_ANS = "[invalid]"

ADD_PARENTHESES_AFTER_KEYWORD = ["sqrt", "frac"]
BAD_SUBSTRINGS = ["^{", "^("]
BAD_REGEXES = ["\^[0-9]+\^", "\^[0-9][0-9]+"]

UNIT_LONG_LIST = [
    "立方厘米",
    "立方分米",
    "平方公里",
    "平方英尺",
    "平方英里",
    "平方英寸",
    "平方英寻",
    "平方英尺",
    "千公里",
    "平方米",
    "立方米",
    "千米",
    "厘米",
    "分米",
    "海里",
    "毫米",
    "公里",
    "英里",
    "公尺",
    "英尺",
    "元",
    "分",
    "角",
    "米",
    "度",
    "里",
    "升",
    "centimeter",
    "second",
    "degree",
    "dollar",
    "minute",
    "radian",
    "square",
    "pound",
    "month",
    "units",
    "meter",
    "edges",
    "mile",
    "hour",
    "year",
    "cent",
    "foot",
    "feet",
    "inch",
    "yard",
    "week",
    "day",
    "rad",
    "mph",
]

UNIT_SHORT_LIST = [
    "eV",
    "kg",
    "mg",
    "km",
    "cm",
    "dm",
    "ml",
    "mL",
    "ft",
    "in",
    "a.m.",
    "p.m.",
    "A.M.",
    "P.M.",
    "am",
    "AM",
    "PM",
    "pm",
]

UNIT_SINGLE_LIST = [
    "L",
    "l",
    "m",
    "g",
]

UNIT_LIST = UNIT_LONG_LIST + UNIT_SHORT_LIST + UNIT_SINGLE_LIST
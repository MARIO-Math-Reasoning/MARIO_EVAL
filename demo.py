from typing import Optional

from math_evaluation import (
    string_normalize,
    are_equal_under_sympy,
    is_equiv,
)


if __name__ == "__main__":
    # example
    
    ground_truth = "(0, 1)"
    prediction = "x=0, y=1"
    eval_res = is_equiv(ground_truth, prediction)
    print(eval_res)   

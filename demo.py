from typing import Optional, List, Union

from math_evaluation import (
    string_normalize,
    are_equal_under_sympy,
    is_equiv,
    is_equiv_type,
)


def is_equiv_MATH(
    ground_truth: Union[str, List[str]],
    prediction: str,
    verbose: bool = False,
) -> bool:
    """
    We manually annotated the ground-truth of MATH testset.

    For some questions, one solution of the provided answers is also considered as correct.
    """
    if isinstance(ground_truth, list):
        for grt in ground_truth:
            if is_equiv(grt, prediction, verbose):
                return True
        return False
    else:
        assert isinstance(ground_truth, str)
        return is_equiv(ground_truth, prediction, verbose)


if __name__ == "__main__":
    assert is_equiv_type("1,234", "(1,234)", "Vector")

    """
    Example:

    "index": 2913,
    "question": "Find the coordinates of either of the vertices of the hyperbola \\[16x^2+16x-4y^2-20y-85=0.\\](Enter your answer as an ordered pair. Enter the coordinates of one of the vertices, not both.",
    "analysis": "To find the standard form for the equation of the hyperbola, we complete the square in both variables: \\[\\begin{aligned} 16(x^2+x) - 4(y^2+5y) - 85  &= 0 \\\\ 16(x^2+x+\\tfrac14)-4(y^2+5y+\\tfrac{25}4) - 85 &= 4 - 25 \\\\ 16(x+\\tfrac12)^2 - 4(y+\\tfrac52)^2 &= 64 \\\\ \\frac{(x+\\tfrac12)^2}{4} - \\frac{(y+\\tfrac52)^2}{16} &= 1. \\end{aligned}\\]Therefore, the center of the hyperbola is the point $\\left(-\\tfrac12, -\\tfrac52\\right).$ The vertices lie to the left and right of the center, and the distance from the center to each vertex is $\\sqrt{4} = 2.$ Thus, the vertices have coordinates \\[\\left(-\\tfrac12 \\pm 2,-\\tfrac52\\right) = \\boxed{\\left(\\tfrac32, -\\tfrac52\\right)} \\text{ and } \\left(-\\tfrac52, -\\tfrac52\\right).\\](Either point is a correct answer to this problem.)", "analysis.original": "To find the standard form for the equation of the hyperbola, we complete the square in both variables: \\[\\begin{aligned} 16(x^2+x) - 4(y^2+5y) - 85  &= 0 \\\\ 16(x^2+x+\\tfrac14)-4(y^2+5y+\\tfrac{25}4) - 85 &= 4 - 25 \\\\ 16(x+\\tfrac12)^2 - 4(y+\\tfrac52)^2 &= 64 \\\\ \\frac{(x+\\tfrac12)^2}{4} - \\frac{(y+\\tfrac52)^2}{16} &= 1. \\end{aligned}\\]Therefore, the center of the hyperbola is the point $\\left(-\\tfrac12, -\\tfrac52\\right).$ The vertices lie to the left and right of the center, and the distance from the center to each vertex is $\\sqrt{4} = 2.$ Thus, the vertices have coordinates \\[\\left(-\\tfrac12 \\pm 2,-\\tfrac52\\right) = \\boxed{\\left(\\tfrac32, -\\tfrac52\\right)} \\text{ and } \\boxed{\\left(-\\tfrac52, -\\tfrac52\\right)}.\\](Either point is a correct answer to this problem.)", 
    "answer": [
        "\\left(\\tfrac32, -\\tfrac52\\right)",
        "\\left(-\\tfrac52, -\\tfrac52\\right)"
    ],
 
    """
  
    ground_truth = ["\\left(\tfrac32, -\\tfrac52\\right)", "\\left(-\\tfrac52, -\\tfrac52\\right)"]
    prediction = "(-2.5,-2.5)"
    eval_res = is_equiv_MATH(ground_truth, prediction, verbose=False)
    assert eval_res

    # Another interesting example     
    ground_truth = "1"
    prediction = "-(-1)^\\frac{{57}}{{85}}\\left({1}+{e}^{{\\frac{{14}}{{85}}}{i}\\pi}\\right)\\left({1}+{e}^{{\\frac{{28}}{{85}}}{i}\\pi}\\right)\\left({1}+{e}^{{\\frac{{46}}{{85}}}{i}\\pi}\\right)\\left({1}+{e}^{{\\frac{{54}}{{85}}}{i}\\pi}\\right)\\left({1}+{e}^{{\\frac{{56}}{{85}}}{i}\\pi}\\right)\\left({1}+{e}^{{\\frac{{58}}{{85}}}{i}\\pi}\\right)\\left({1}+{e}^{{\\frac{{62}}{{85}}}{i}\\pi}\\right)\\left({1}+{e}^{{\\frac{{78}}{{85}}}{i}\\pi}\\right)"
    eval_res = is_equiv_MATH(ground_truth, prediction, verbose=False)
    assert eval_res

    # Let's verify it
    from latex2sympy.latex2sympy2 import latex2sympy
    import sympy as sp

    prediction = prediction.replace("{i}", "{I}")
    pred_val = latex2sympy(prediction)
    print("ground_truth: ", ground_truth)
    print("prediction: ", pred_val)
    print("Re of prediction: ", sp.re(pred_val).evalf())
    print("Im of prediction: ", sp.im(pred_val).evalf())

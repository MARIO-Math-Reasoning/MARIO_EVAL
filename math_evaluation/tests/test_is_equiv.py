import unittest
import sys

from math_evaluation import (
    string_normalize,
    are_equal_under_sympy,
    is_equiv,
)


def _test_is_equiv(test_in, test_out, verbose=False):
    output = is_equiv(test_in, test_out, verbose=verbose)
    if not output:
        print(f"Test not passed: {test_in} == {test_out}")
    return output


def _test_is_not_equiv(test_in, test_out, verbose=False):
    output = is_equiv(test_in, test_out, verbose=verbose)
    if output:
        print(f"Test not passed: {test_in} != {test_out}")
    return output


class TestIsEquiv(unittest.TestCase):

    def test_are_equal_under_sympy(self):
        verbose = False

        # set
        test_in = "{x, x - 1}"
        test_out = "{x - 1, x}"
        self.assertTrue(is_equiv(test_in, test_out, verbose=verbose))

        # complex
        test_in = "x + \\sqrt2I"
        test_out = "x + 1.414I"
        self.assertTrue(is_equiv(test_in, test_out, verbose=verbose))

    def test_is_equiv_real_or_list(self):
        verbose = False

        test_in = "11,\! 111,\! 111,\! 100"
        test_out = "11111111100"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

        test_in = "1 1/2"
        test_out = "1.5"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

        test_in = "4210_{7}"
        test_out = "4210_7"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

        test_in = "1\\frac12"
        test_out = "1.5"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

        test_in = "2\\frac58"
        test_out = "2.625"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

        test_in = ".1, 4.0"
        test_out = "0.1, 4"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

        test_in = "10\\%"
        test_out = "10"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

        test_in = "10\\%"
        test_out = "0.1"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

        test_in = "\\frac13, \\sqrt3, \\pi"
        test_out = "1/3, 1.732, 3.1416"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

        test_in = "40\\pi"
        test_out = "125.663"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

        test_in = "1, 2, 3"
        test_out = "1, 3, 2"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

        test_in = "7, -2, \\text{ and } -5"
        test_out = "-5,-2,7"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

        test_in = "[1, 2, 3]"
        test_out = "(1, 3, 2)"
        self.assertFalse(_test_is_not_equiv(test_in, test_out, verbose=verbose))

        test_in = "[x, x + 1]"
        test_out = "[x, 1 + x]"
        self.assertTrue(are_equal_under_sympy(test_in, test_out, verbose=verbose))

        test_in = "[x, x + 1]"
        test_out = "[x + 1, x]"
        self.assertFalse(are_equal_under_sympy(test_in, test_out, verbose=verbose))

    def test_is_equiv_complex(self):
        verbose = False

        # for small i, only support expression without other unknown variables.
        test_in = "1+2i"
        test_out = "i(2-i)"
        self.assertTrue(are_equal_under_sympy(test_in, test_out, verbose=verbose))

    def test_is_fraction(self):
        verbose = False

        # other fraction
        test_in = "\\tfrac23 +\\frac1{72}"
        test_out = "\\\\dfrac{2}{3} +\\frac{1}{72}"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

        test_in = "$\\frac{\\sqrt{17}}{17}$"
        test_out = "$\\frac{\\sqrt{17}}{17}$"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

        test_in = "$\\frac{4\\sqrt{5}}{5}$"
        test_out = "$\\frac{4\\sqrt{5}}{5}$"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

        test_in = "\\frac{\\sqrt{3}}{2}"
        test_out = "0.8660254037844386"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

    def test_is_equiv_units(self):
        verbose = False

        test_pairs = [
            ("10\\text{ units}", "10"),
            ("10 square units", "10"),
            ("10 \\text{cm}", "10"),
            ("10\\text{ cm}^2", "10"),
            ("10\\text{ cm}^{2}", "10"),
            ("10weeks", "10"), # space is optional for long unit
            ("10 weeks", "10"),
            ("10 cm^2", "10"), # space is must for short unit
            ("20:34", "20:34:00"),
            ("20:34", "08:34 \\text{P.M.}"),
        ]
        for test_in, test_out in test_pairs:
            self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

        test_pairs = [
            ("10cm", "10"),
            ("10m", "10"),
        ]
        for test_in, test_out in test_pairs:
            self.assertFalse(_test_is_not_equiv(test_in, test_out, verbose=verbose))

        test_in = "10"
        test_out = "\\$10"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

    def test_is_equiv_parentheses(self):
        verbose = False

        test_in = "\\left(x-2\\right)\\left(x+2\\right)"
        test_out = "(x-2)(x+2)"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

    def test_is_equiv_sqrt(self):
        verbose = False

        test_in = "10\\sqrt{3} + \\sqrt4"
        test_out = "10\\sqrt3 + \\sqrt{4}"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

        test_in = "$\\sqrt{5}$"
        test_out = "$\\\\sqrt{5}$"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

    def test_is_equiv_equation(self):
        verbose = False

        test_in = "5x - 7y + 11z + 4 = 0"
        test_out = "x + y - z + 2 = 0"
        self.assertFalse(_test_is_not_equiv(test_in, test_out, verbose=verbose))

        test_in = "\\sin(x)=\\frac{42}{59}"
        test_out = "\\cos(x)=\\frac{42}{59}"
        self.assertFalse(_test_is_not_equiv(test_in, test_out, verbose=verbose))

    def test_is_equiv_expression(self):
        verbose = False

        test_in = "$\\frac{v_{0}}{r_{0}} \\frac{1}{\\left(1+r / r_{0}\\right)^{3 / 2}}$"
        test_out = "$\\frac{v_0 \\cdot \\left(\\frac{r_0}{r + r_0}\\right)^{0.5}}{(r + r_0)}$"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

        test_in = "11z^{7}(5+11z^{7})"
        test_out = "11z^7(11z^7+5)"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

        test_in = "$\\frac{8-7x}{6}$"
        test_out = "$4/3-7x/6$"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

        test_in = "(2x+3)(2x -1)(2x+1)"
        test_out = "(2x - 1)(2x + 1)(2x + 3)"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

        test_in = "2^6 * 3^5 * 5^4"
        test_out = "2^6 3^5 5^4"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

    def test_is_equiv_matrix(self):
        verbose = False

        test_in = "\\begin{pmatrix} 1 & 1/2 \\\\ 1/3 & 4 \\end{pmatrix}"
        test_out = "\\begin{pmatrix} 1 & 0.5 \\\\ 1/3 & 4 \\end{pmatrix}"
        # test_out="$\\\\begin{pmatrix} 6 \\\\\\\\ 3 \\\\\\\\ 0 \\\\end{pmatrix}$"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

        test_in = "\\begin{matrix} x \\\\ \\sqrt{3} + 2x  \\\\ \\frac12 \\end{matrix}"
        test_out = "\\begin{matrix} x \\\\ \\sqrt{3} + 2x \\\\ 0.5 \\end{matrix}"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

        test_in = "\\\\begin{matrix} x \\\\\\\\ \\\\sqrt{3} + 2I  \\\\\\\\ \\\\frac12 \\\\end{matrix}"
        test_out = "\\begin{matrix} x \\\\ \\sqrt{3} + 2I \\\\ 0.5 \\end{matrix}"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

        test_in = "\\begin{matrix} \\frac12 \\\\ 1 \\end{matrix}"
        test_out = "[0.5, 1]"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

        test_in = "\\begin{cases} a+b=\\frac12 \\\\ a-b=\\sqrt3 \\end{cases}"
        test_out = "\\begin{cases} a+b=0.5\\\\ a-b=1.732\\end{cases}"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

    def test_is_equiv_trigonometric(self):
        verbose = False

        test_in = "\\sec x"
        test_out = "\\frac1{\\cos x}"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

        test_in = "\\sin(90^{\\circ}-x)"
        test_out = "\\cos(x)"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

    def test_is_equiv_scinot(self):
        verbose = False

        test_in = "2.314814814815 \\times 10^{-3}"
        test_out = "\\frac{1}{432}"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

    def test_is_equiv_interval(self):
        verbose = False

        test_in = "x \\in [0.5, \\infty)"
        test_out = "[1/2, \\infty)"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

        test_in = "[1,+\\infty)"
        test_out = "[2^{\\frac{1}{2^{1000}}}, \\infty)"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

        test_in = "[-3,2]"
        test_out = "(-3,2)"
        self.assertFalse(_test_is_not_equiv(test_in, test_out, verbose=verbose))

        test_in = "[1, 2)"
        test_out = "[x, y)"
        self.assertFalse(_test_is_not_equiv(test_in, test_out, verbose=verbose))

    def test_is_equiv_coordinate(self):
        verbose = False

        test_in = "x = 1, y = 2, z = 3"
        test_out = "1, 2, 3"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))

    def test_is_equiv_function(self):
        verbose = False

        test_in = "f(x) = 2x + 3"
        test_out = "2x + 3"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))
        test_out = "y = 2x + 3"
        self.assertTrue(_test_is_equiv(test_in, test_out, verbose=verbose))


if __name__ == '__main__':
    unittest.main()

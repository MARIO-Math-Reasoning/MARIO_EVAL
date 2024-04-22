from .context import assert_equal
import pytest
from sympy import Sum, I, Symbol, Integer

a = Symbol('a')
b = Symbol('b')
i = Symbol('i')
n = Symbol('n')
x = Symbol('x')


def test_complex():
    assert_equal("a+Ib", a + I * b)


def test_complex_e():
    assert_equal("e^{I\\pi}", Integer(-1))


def test_complex_sum():
    assert_equal("\\sum_{i=0}^{n} i \\cdot x", Sum(i * x, (i, 0, n)))

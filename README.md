# MATH EVALUATION

## We fix some bugs in the original latex2sympy, and more antlr parser syntax to support more latex expressions.

## Requirements
1. `sympy=1.12`
2. `antlr4-python3-runtime==4.11.1`


## Use without install
```
> git clone https://github.com/MARIO-Math-Reasoning/math_evaluation.git
> cd math_evaluation
> python
>>> from latex2sympy.latex2sympy2 import latex2sympy
>>> latex2sympy("\\frac12")
1/2
>>> from math_evaluation import is_equiv 
>>> is_equiv("\\frac12", "0.5")
True
```

## Install as Python package
```
> git clone https://github.com/MARIO-Math-Reasoning/math_evaluation.git
> cd math_evaluation
> cd latex2sympy && pip install . && cd ..
> pip install -e .
```

## Unittest
`python -m unittest math_evaluation/tests/test_is_equiv.py`

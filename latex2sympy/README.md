# Fork and modify from [latex2sympy2](https://github.com/OrangeX4/latex2sympy/tree/master)

## Using the original latex2sympy2
```python
from latex2sympy2_orig import latex2sympy

latex2sympy(r"\frac{1}{2}")
```

## BUG fix in  the modified version
```python
from latex2sympy2 import latex2sympy

latex2sympy(r"\frac12")

latex2sympy(r"\frac{d}{dx} \tan x")

latex2sympy(r"d x_{10}")

latex2sympy(r"\frac{d}{dx_1} \tan x_1")

latex2sympy(r"\sqrt3")

latex2sympy(r"\emptyset")

# cannot run twice in origianl version
latex2sympy("\\int(x dx)")
latex2sympy("\\int(x dx)")
```
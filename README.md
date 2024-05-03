# MARIO EVAL: A mathematical dataset evaluation toolkit

This is the official repository for the paper [MARIO Eval](https://arxiv.org/abs/2404.13925). We fix some bugs in the original latex2sympy, and add more antlr parser syntax to support more latex expressions.

## Features
- [x] sympy based equivalence of two math expressions, see `is_equiv`
- [x] annotation of MATH testset with more robust evaluation, see `data/math_testset_annotation.json` and `demo.py`
- [ ] integration of LLM (coming soon)

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

## Evaluation on [MATH](https://github.com/hendrycks/math) dataset
| Model                     | Accuracy |
| ------------------------- | -------- |
| [ToRA-Code-34B](https://github.com/microsoft/ToRA/tree/aeb21126d28347f595d87f2822cb92bfe32f00e8/src/outputs/llm-agents/tora-code-34b-v1.0/math)  | 0.5122 |
| [ToRA-70B](https://github.com/microsoft/ToRA/tree/aeb21126d28347f595d87f2822cb92bfe32f00e8/src/outputs/llm-agents/tora-70b-v1.0/math) | 0.5002 |
| [DeepSeek-Math-Instruct-7B](https://github.com/deepseek-ai/DeepSeek-Math/blob/main/evaluation/outputs.zip) | 0.5722 |


## Unittest
`python -m unittest math_evaluation/tests/test_is_equiv.py`

## Citation
Please cite our paper if you use data or code.
```
@misc{zhang2024mario,
      title={MARIO Eval: Evaluate Your Math LLM with your Math LLM--A mathematical dataset evaluation toolkit}, 
      author={Boning Zhang and Chengxi Li and Kai Fan},
      year={2024},
      eprint={2404.13925},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

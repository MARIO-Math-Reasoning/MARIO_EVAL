# MARIO EVAL: A mathematical dataset evaluation toolkit

This is the official repository for the paper [MARIO Eval](https://arxiv.org/abs/2404.13925). We fix some bugs in the original latex2sympy, and add more antlr parser syntax to support more latex expressions.

## Evaluation on [MATH](https://github.com/hendrycks/math) dataset
| Model                     | Accuracy | Reported |
| ------------------------- | -------- | -------- |
| [MathCoder-CL-7B](https://github.com/mathllm/MathCoder/blob/77b46cd80399b488c8432c4cb6d645369749f7b5/outs/MathCoder-CL-7b/MATH/MATH_test_result-20230917-1756.jsonl) | 0.3064 | [0.3074](https://github.com/mathllm/MathCoder/tree/77b46cd80399b488c8432c4cb6d645369749f7b5/outs/MathCoder-CL-7b) |
| [MathCoder-CL-34B](https://github.com/mathllm/MathCoder/blob/77b46cd80399b488c8432c4cb6d645369749f7b5/outs/MathCoder-CL-34b/MATH/MATH_test_result-20230916-0325.jsonl) | 0.4584 | [0.461](https://github.com/mathllm/MathCoder/tree/77b46cd80399b488c8432c4cb6d645369749f7b5/outs/MathCoder-CL-34b/MATH) |
| [ToRA-Code-34B](https://github.com/microsoft/ToRA/tree/aeb21126d28347f595d87f2822cb92bfe32f00e8/src/outputs/llm-agents/tora-code-34b-v1.0/math)  | 0.5136 | [0.51](https://github.com/microsoft/ToRA/blob/aeb21126d28347f595d87f2822cb92bfe32f00e8/src/outputs/llm-agents/tora-code-34b-v1.0/math/test_tora_-1_seed0_t0.0_s0_e5000.metrics) |
| [ToRA-70B](https://github.com/microsoft/ToRA/tree/aeb21126d28347f595d87f2822cb92bfe32f00e8/src/outputs/llm-agents/tora-70b-v1.0/math) | 0.5014 | [0.497](https://github.com/microsoft/ToRA/blob/aeb21126d28347f595d87f2822cb92bfe32f00e8/src/outputs/llm-agents/tora-70b-v1.0/math/test_tora_-1_seed0_t0.0_s0_e5000.metrics) |
| [DeepSeek-Math-Base-7B](https://github.com/deepseek-ai/DeepSeek-Math/tree/21cc5c6701a708a11cee0af8b1fe884e3294dc7a/evaluation) | 0.3318 | [0.3142](https://github.com/deepseek-ai/DeepSeek-Math/tree/21cc5c6701a708a11cee0af8b1fe884e3294dc7a/evaluation) |
| [DeepSeek-Math-Instruct-7B](https://github.com/deepseek-ai/DeepSeek-Math/tree/21cc5c6701a708a11cee0af8b1fe884e3294dc7a/evaluation) | 0.572 | [0.575](https://github.com/deepseek-ai/DeepSeek-Math/tree/21cc5c6701a708a11cee0af8b1fe884e3294dc7a/evaluation) |
| [DeepSeek-Math-RL-7B](https://github.com/deepseek-ai/DeepSeek-Math/tree/21cc5c6701a708a11cee0af8b1fe884e3294dc7a/evaluation) | 0.596 | [0.5878](https://github.com/deepseek-ai/DeepSeek-Math/tree/21cc5c6701a708a11cee0af8b1fe884e3294dc7a/evaluation) |

## Features
- [x] sympy based equivalence of two math expressions, see `is_equiv`
- [x] annotation of MATH testset with more robust evaluation, see `data/math_testset_annotation.json` and `demo.py`
- [x] integration of LLM

## Requirements
1. `sympy=1.13.1`
2. `antlr4-python3-runtime==4.11.1`
    - If `omegaconf` needed, please `pip install omegaconf==2.4.0.dev3`
    - If `hydra-core` needed, please install from source for the latest version `git clone https://github.com/facebookresearch/hydra.git` 
3. **NOT** install `gmpy2`, i.e., `pip uninstall gmpy2`


## Use without install
```
> git clone https://github.com/MARIO-Math-Reasoning/MARIO_EVAL.git
> cd MARIO_EVAL
> python
>>> from latex2sympy.latex2sympy2 import latex2sympy
>>> latex2sympy("\\frac12")
1/2
>>> from math_evaluation import is_equiv 
>>> is_equiv("1\\frac12", "1.5")
True
>>> is_equiv("\\begin{pmatrix} 1 & \\frac12 \\\\ 1/3 & \\sqrt4 \\end{pmatrix}", 
...          "[[1.0, 1/2],[0.3333, 2.0]]")
True
```

## Install as Python package
```
> git clone https://github.com/MARIO-Math-Reasoning/MARIO_EVAL.git
> cd MARIO_EVAL
> cd latex2sympy && pip install . && cd ..
> pip install -e .
```

## Unittest
`python -m unittest math_evaluation/tests/test_is_equiv.py`

Please wait for about 20 seconds, because timeout test needs 15 (default) seconds.

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

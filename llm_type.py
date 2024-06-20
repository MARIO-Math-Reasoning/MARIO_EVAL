import os

if not os.environ.get("DASHSCOPE_API_KEY"):
    raise ValueError("In you shell, run `export DASHSCOPE_API_KEY=...`")

from tqdm import tqdm
from typing import Any, Dict, List
from math_evaluation.llms import (
    create_llm,
    get_llm_type,
)


if __name__ == '__main__':
    # example 

    # load data
    # json_file = ""
    # with open(json_file, "r") as f:
    #     data = json.load(f)
    #     if len(data) > 0:
    #         assert "question" in data[0] and "answer" in data[0]

    data = [
        {
            "question": "What is the coordinate of line $y = x + 2$ intercepting with y-aixs.",
            "answer": "(0, 2)",
        },
        {
            "question": "Given $|x - 1| < 1$, solve $x$.",
            "answer": "(0, 2)"
        }
    ]

    call_llm = create_llm("tongyi", "qwen-max")
    for d in tqdm(data):
        answer_type = get_llm_type(
            call_llm, 
            d["question"],
            d["answer"],
        )
        print(answer_type)



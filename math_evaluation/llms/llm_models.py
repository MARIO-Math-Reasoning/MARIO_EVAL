import os
import re
from typing import Optional, Callable
from functools import partial

from .prompts import prompt_template, prompt_template_2


def call_tongyi(messages, client, model):
    response = client.call(
        model=model,
        messages=messages,
        temperature=0.0001,
    )
    return response.output.text


def call_openai(messages, client, model):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.0001,
    )
    return response.choices[0].message.content


def create_llm(llm: str = "openai", model: str = "gpt-3.5-turbo"):
    if llm == "openai":
        import openai
        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OPENAI_API_KEY key if not set as env var>"))
        call_llm = call_openai

    elif llm == "tongyi":
        import dashscope
        dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY", "<your DASHSCOPE_API_KEY if not set as env var>")
        client = dashscope.Generation
        call_llm = call_tongyi

    else:
        raise ValueError(f"llm can only be one of [openai, tongyi].")

    return partial(call_llm, client=client, model=model)


def get_llm_type(
    call_llm: Callable,
    question: str,
    answer: str,
    prompt_type: int = 1,
    max_try: int = 5,
) -> Optional[str]:
    # format answer
    if not (answer.startswith("$") and answer.endswith("$") and answer.count("$") == 2):
        answer = "${ans}$".format(ans=answer.replace("$", ""))

    # select prompt_template
    if prompt_type == 1:
        prompt = prompt_template.format(question=question, ground_truth=answer)
    elif prompt_type == 2:
        prompt = prompt_template_2.format(question=question, ground_truth=answer)
    else:
        raise ValueError("not defined prompt type")

    # compose messages
    messages = [
        {"role": "user", "content": prompt},
    ]

    # run llm for answer type
    retry = 0
    answer_type = None
    while retry < max_try:
        try:
            resp_text = call_llm(messages)
            answer_type = re.search(r"Type:[\s]*(.*)", resp_text).group(1)
            break
        except:
            retry += 1

    return answer_type
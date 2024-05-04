import os
import json
from tqdm import tqdm

from demo import is_equiv_MATH

tora_file = "../tora_code_34b_math.jsonl"
#tora_file = "../tora_70b_math.jsonl"

if not os.path.exists(tora_file):
    print("Download model output from `https://github.com/microsoft/ToRA/tree/main/src/outputs/llm-agents`.")
    exit(1)

tora_data = []
with open(tora_file, "r") as f:
    for line in f:
        tora_data.append(json.loads(line.strip()))

test_file = "data/math_testset_annotation.json"
with open(test_file, "r") as f:
    test_data = json.load(f)
assert len(tora_data) == len(test_data)

q2a = {}
for t_d in test_data:
    question = t_d["question"]
    answer = t_d["answer"]
    q2a[question] = answer

def extract_boxed(output):
    lidx = output.rfind("\\boxed{")
    if lidx > 0:
        lidx += len("\\boxed{")
        ridx = output.rfind("}")
        return output[lidx: ridx]
    return None

cnt = 0
for i, tora_d in enumerate(tqdm(tora_data)):
    question = tora_d["question"]
    # use our annotation, rather than tora_d["gt"]
    answer = q2a[question]
    # extract prediction, rather than tora_d["prediction"][-1]
    prediction = extract_boxed(tora_d["code"][-1])
    if prediction is not None and is_equiv_MATH(answer, prediction):
        cnt += 1

print(cnt / len(tora_data))

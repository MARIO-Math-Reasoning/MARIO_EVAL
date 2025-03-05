import os

from typing import Union, List, Tuple, Optional
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from tqdm import tqdm
from pebble import ProcessPool

from math_evaluation import is_equiv
from timeout_decorator import timeout


def math_eval(params):
    prediction, ground_truth = params

    if isinstance(ground_truth, str):
        ground_truth = [ground_truth]  

    for grt in ground_truth:
        if is_equiv(grt, prediction, verbose=False, fast=True):
            return True
    return False

    
class EvaluationProxy:
    def __init__(self):
        self.timeout = 30

    def get_result(self, 
        solution: List[str], 
        ground_truth: List[Union[str, List[str]]],
        **kwargs
    ):
        assert len(solution) == len(ground_truth), "should have same lengths"

        batch_data = list(zip(solution, ground_truth))

        results = []
        with ProcessPool(max_workers=min(len(batch_data), os.cpu_count())) as pool:
            futures = [pool.schedule(math_eval, args=(data,), timeout=self.timeout) for data in batch_data]
            with tqdm(total=len(batch_data), desc='Processing') as pbar:
                for future in futures:
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        print("{}: {}".format(type(e).__name__, str(e)))
                        results.append(False)
                    pbar.update(1)
    
        return results


# create FastAPI app
def create_app():
    eval_proxy = EvaluationProxy()
    app = FastAPI()

    @app.post("/get_result")
    async def get_eval_result(request: Request):
        data = await request.json()
        predictions = data.get("predictions")
        answers = data.get("answers")
        results = eval_proxy.get_result(predictions, answers)
        result = {"result": results}
        return JSONResponse(result)

    return app


app = create_app()
import ray
import logging

from ray_utils import remote_rm_fn, remote_rm_fn_ray

api_url = "http://0.0.0.0:5000/get_result"

predictions = ["\\frac12", "1.414", "2", "x + 1"]
answers = ["0.5", "\\sqrt2", "\\sqrt3", "1 + x"]

# results = remote_rm_fn(api_url, predictions=predictions, answers=answers)
# print(results)

if ray.is_initialized:
    ray.shutdown()
ray.init(logging_level=logging.ERROR)

ray_results = remote_rm_fn_ray.remote(api_url, predictions=predictions, answers=answers)
results = ray.get(ray_results)
print(results)

import time
import ray
import requests


def request_api_wrapper(url, data, result_key="result", try_max_times=5):
    """Synchronous request API wrapper"""
    headers = {
        "Content-Type": "application/json",
    }
    for _ in range(try_max_times):
        try:
            response = requests.post(url=url, json=data, headers=headers, timeout=180)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            response = response.json()
            assert result_key in response, f"{result_key} not in {response}"
            return response.get(result_key)
        except requests.RequestException as e:
            print(f"Request error, please check: {e}")
        except Exception as e:
            print(f"Unexpected error, please check: {e}")
        time.sleep(1)

    raise Exception(f"Request error for {try_max_times} times in url: {url}, returning None. Please check the API server.")


def remote_rm_fn(api_url, predictions, answers, result_key="result"):
    results = request_api_wrapper(api_url, {"predictions": predictions, "answers": answers}, result_key)
    return results


@ray.remote
def remote_rm_fn_ray(api_url, predictions, answers, result_key="result"):
    return remote_rm_fn(api_url, predictions, answers, result_key=result_key)


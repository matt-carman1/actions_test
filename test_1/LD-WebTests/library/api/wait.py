import time
from typing import Callable


def wait_until_condition_met(condition_function: Callable, retries: int = 60, interval: int = 1000):
    for i in range(retries):
        try:
            condition_function()
            return
        except AssertionError as e:
            if i == retries - 1:
                raise e
            time.sleep(interval / 1000)

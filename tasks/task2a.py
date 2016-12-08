from time import sleep
from random import randint
import timeit


def slow_log(max_time):
    def decorator(f):
        def wrapper(*args, **kwargs):
            st = timeit.default_timer()
            res = f(*args, **kwargs)
            exec_time = timeit.default_timer() - st
            if exec_time > max_time:
                print(exec_time)
            return res
        return wrapper
    return decorator


@slow_log(5)
def f():
    delay = randint(1, 10)
    sleep(delay)

if __name__ == "__main__":
    f()

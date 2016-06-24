from timeit import timeit
import time
import signal

start_time = timeit()
for i in range(500):
    pass

end_time = timeit()
elasp = end_time - start_time


class TimeoutError(Exception):
    def __init__(self, value="Time Out"):
        self. value = value

    def __str__(self):
        return repr(self.value)


def time_out_decorator():
    TO = 10
    def handle(signum, frame): # arguments are required by the signal module
        raise TimeoutError("time out error")
        exit(0)

    def decorator(function, *args, **kwargs):
        old = signal.signal(signal.SIGALRM, handle)
        signal.alarm(TO)    # set up a timeout schedule
        try:
            result = function(*args, **kwargs)
        finally:
            signal.signal(signal.SIGALRM, old)  # just redirect to the old handler.
        signal.alarm(0)     # set time of signal.alarm(time) to be 0 will cancel the timeout schedule
        return result

    return decorator


@time_out_decorator()
def time_test():
    time.sleep(15)








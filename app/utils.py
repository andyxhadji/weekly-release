import time
from func_timeout import func_timeout, FunctionTimedOut


def get_week(today):
    # Will never return 0, will return 13 instead
    return (today.isocalendar()[1] % 13) or 13

def get_quarter(today):
    return (today.month - 1) // 3 + 1

def get_year(today):
    # This will break in year 2100
    return today.year % 100

def handler(signum, frame):
    print("Signal timeout handler")
    raise Exception("Timeout handler")

def poll_api(tries=5, delay=5, api_function=None, args=[], kwargs={}):

    for n in range(tries):
        try:
            api_output = func_timeout(10, api_function, args=args, kwargs=kwargs)
            return api_output
        except (FunctionTimedOut, Exception) as e:
            print(e)
            if (n + 1) == tries:
                raise Exception("Too many retries!")
            else:
                time.sleep(delay)
                print("Retry #{}...".format(n))

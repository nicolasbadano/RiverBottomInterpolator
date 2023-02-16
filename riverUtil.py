from itertools import tee


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def print_decorate(func):
    def wrapper(*args, **kwargs):
        print("INFO: ENTERED %s" % func.__name__)
        ret = func(*args, **kwargs)
        print("INFO: EXITED %s" % func.__name__)
        return ret
    return wrapper

import multiprocessing
from r2_stringmatching import stringmatching
from r3_FunctionAnalysis import FunctionAnalysis


def multiprocess():
    pool = multiprocessing.Pool()
    result = []

    result.append(pool.apply_async(FunctionAnalysis).get())
    result.append(pool.apply_async(stringmatching).get())

    pool.close()
    return result


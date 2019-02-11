import traceback
import random
from collections import defaultdict
import operator


def verbose_f(f):
    #f.height = 0
    def result_f(*args):
        #f.height += 1
        height = sum([f.__name__ in str(item) for item in list(traceback.extract_stack())])
        #print(f.__name__)
        #print(list(traceback.extract_stack()))
        #print([f.__name__ in item for item in list(traceback.extract_stack())])
        print(f.__name__ + str(height) + ' input:' + str(args))
        result = f(*args)
        print(f.__name__ + str(height) + ' output:' + str(result))
        #f.height -= 1
        return result
    return result_f


def count(x):
    result = defaultdict(int)
    for item in x:
        result[item] += 1
    return result


def join_list(xs, ys, f=operator.add):
    return [f(x, y) for x in xs for y in ys]


def pair_adder(x, y):
    return x[0]+y[0], x[1]+y[1]


def assert_eq(res, gt):
    assert res == gt, str(res) + ' should be equal to ' + str(gt)


def assert_same(x):
    assert len(count(x).keys()) == 1, str(x) + ' should have only one type'

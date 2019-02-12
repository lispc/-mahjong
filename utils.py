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


def cache_f(f):
    d = {}
    def result_f(*args):
        if args in d:
            return d[args]
        result = f(*args)
        d[args] = result
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


def list_sub(a, b):
    sorted_a = sorted(a)
    sorted_b = sorted(b)
    result = []
    for i in sorted_a:
        if i not in sorted_b:
            result.append(i)
        else:
            idx = sorted_b.index(i)
            del sorted_b[idx]
    return result


def dict_sub(a, b):
    result = {}
    for k in a:
        if k in b:
            assert a[k] >= b[k], str(k) + ' ' + str(a) + ' ' + str(b)
            if a[k] - b[k] != 0:
                result[k] = a[k] - b[k]
        else:
            result[k] = a[k]
    return result

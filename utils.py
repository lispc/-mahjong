import traceback
import random


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


def assert_eq(res, gt):
    assert res == gt, str(res) + ' should be equal to ' + str(gt)


def rand_card():
    invalid_set = set([10,20,30])
    candidate = random.randrange(1,38)
    while candidate in invalid_set:
        candidate = random.randrange(1,38)
    return candidate

def rand_single_color(l=13):
    cnt = 0
    d = {}
    while cnt < l:
        candidate = random.randrange(1, 10)
        if candidate not in d:
            d[candidate] = 0
        if d[candidate] == 4:
            continue
        d[candidate] += 1
        cnt += 1
    result = []
    for k, v in sorted(d.items()):
        result += [k]*v
    return result

def rand_seq(l=13):
    return [rand_card() for _ in range(l)]

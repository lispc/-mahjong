from constants import *
from utils import *
from algo import *


@verbose_f
def split_by_category(x):
    sorted_x = sorted(x)
    result = [[], [], [], []]
    for item in x:
        result[item//10].append(item)
    return result


def max_unit(x):
    slices = split_by_category(x)
    return 0


def test_max_unit():
    assert_eq(max_unit([wan2, wan2, wan2, wan2, wan3, wan3, wan3, wan3, wan4, wan4, wan4, wan4]), 4)


def test_scatter():
    assert_eq(scatter({'a':2,'b':2},3), [{'a':1,'b':2}, {'a':2,'b':1}])

def test_append():
    assert_eq(multi_append({(1,): 4}, 2, 4), [{(1, 2): 4}])

def test_add():
    sets = ActiveSets()
    #print(repr(sets))
    sets.add(wan1, 4)
    #print(repr(sets))
    sets.add(wan2, 4)
    #print(repr(sets))
    sets.add(wan3, 4)
    #print(repr(sets))
    #print(sets.get_gram_stat())
    assert_eq(sets.max3(), 4)

def max3seq(cards):
    sets = ActiveSets()
    sets.from_list(cards)
    #print(repr(sets))
    #print(sets.get_gram_stat())
    return sets.max3()

def test_max3():
    assert_eq(max3seq([1, 2, 3, 4, 4, 5, 5, 6, 6]), 3)
    assert_eq(max3seq([1, 1, 2, 2, 3, 3]), 2)  # 123 123
    assert_eq(max3seq([1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 6, 6, 9]), 3) # 123 123 345|456
    cnt = 20
    while cnt != 0:
        cnt -= 1
        cards = rand_single_color()
        print(sorted(cards), max3seq(cards))

def test_slice():
    assert_eq(to_slice(1), [
        [1]
    ])
    assert_eq(to_slice(2), [
        [1,1],
        [2]
    ])
    assert_eq(to_slice(3), [
        [1,1,1],
        [2,1],
        [3]
    ])
    assert_eq(to_slice(4), [
                [1,1,1,1],
                [2,1,1],
                [2,2],
                [3,1]
    ])


if __name__ == '__main__':
    #test_slice()
    #test_scatter()
    #test_append()
    #test_add()
    test_max3()
    #test_max_unit()

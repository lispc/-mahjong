from constants import *
from utils import *
from algo import *


def test_max_unit():
    assert_eq(handle_singles([east, east, east, west, west, west]), [(2,0),(1,1),(0,2)])
    cnt = 0
    while cnt != 0:
        cnt -= 1
        cards = rand_seq()
        print(display_cards(cards))
        print(max_unit(cards))


def test_scatter():
    assert_eq(scatter({'a':2,'b':2},3), [{'a':1,'b':2}, {'a':2,'b':1}])


def test_append():
    assert_eq(multi_append({(1,): 4}, 2, 4), [{(1, 2): 4}])


def test_list_sub():
    assert_eq(list_sub([1,2,2,3,3,3,4,4,4,4], [2,2,2,3,3]), [1,3,4,4,4,4])


def test_select():

    def check(seq):
        print('14张牌:', seq)
        print(display_cards(seq))
        #print('建议出牌(算法1):', display_cards(select14(seq, eval_naive), False))
        res = select14(seq, eval2)
        print('建议出牌:')
        for m, c in res[:5]:
            print(card_to_str(c), '%.3f'%m)
        print('')
    while False:
        cards = [6,7,8,11,11,11,12,13,18,18,22,28,2,29]
        check(cards)
        break
        cards = [2, 5, 5, 6, 11, 11, 14, 24, 26, 28, 28, 29, 33, 36]
        check(cards)
        cards = [1, 1, 1, 7, 8, 13, 16, 16, 18, 6, 7, 8, 31, 33]
        check(cards)
        cards = [11,16,18,18,21,21,21,21,26,27,34,36,36,37]
        check(cards)
    cnt = 10
    while cnt != 0:
        cnt -= 1
        cards = rand_seq_no_single(14)
        check(cards)


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
    assert_eq(max3seq([1, 2, 3, 5, 6, 7]), 2)
    assert_eq(max3seq([1, 1, 2, 2, 3, 3]), 2)  # 123 123
    assert_eq(max3seq([1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 6, 6, 9]), 3) # 123 123 345|456
    assert_eq(max3seq([wan2, wan2, wan2, wan2, wan3, wan3, wan3, wan3, wan4, wan4, wan4, wan4]), 4)
    cnt = 0
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
    test_slice()
    test_scatter()
    test_append()
    test_add()
    test_max3()
    test_max_unit()
    test_select()
    test_list_sub()

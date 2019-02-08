from collections import defaultdict
import copy
from utils import *
from constants import *
import operator


def scatter(slots, num):
    if sum(slots.values()) < num:
        return []
    if num == 0:
        return [{k:0 for k in slots}]
    if len(slots) == 0:
        return [{}]
    keys = list(slots.keys())
    results = []
    first_key = keys[0]
    for i in range(0,slots[first_key]+1):  # how many to put in this slot
        if i > num:
            break
        new_slots = {k:slots[k] for k in slots if k != first_key}
        new_num = num - i
        res = scatter(new_slots, new_num)
        for item in res:
            item[first_key] = i
            results.append(item)
    return results


def multi_append(base, item_to_add, item_num):
    if item_num == 0:
        return [copy.deepcopy(base)]
    base_num = sum(base.values())
    if base_num <= item_num:
        result = {k+(item_to_add,): v for k, v in base.items()}
        if base_num < item_num:
            result[(item_to_add,)] = item_num - base_num
        return [result]
    else:
        #keys_num = len(base)
        results = []
        res = scatter(base, item_num)
        for item in res:
            base_clone = copy.deepcopy(base)
            for k, v in item.items():
                if v != 0:
                    base_clone[k + (item_to_add,)] = v
                    base_clone[k] -= v
                    if base_clone[k] == 0:
                        del base_clone[k]
            results.append(base_clone)
        return results


class ActiveSet:
    def __init__(self):
        self.active = {} # tuple -> count
        self.non_active = {}
        self.parent = None

    def __repr__(self):
        return '(' + repr(self.active) + ',' + repr(self.non_active) + ')'

    def strip_dead(self, active_idx):
        for item in list(self.active.keys()):
            if item[-1] != active_idx:
                del self.active[item]

    def freeze(self):
        #print('freeze', repr(self), 'parent', repr(self.parent))
        for item in list(self.active.keys()):
            if len(item) == 3:
                assert item not in self.non_active, repr(item) + ' should not in ' + repr(self.non_active)
                assert self.active[item] != 0
                self.non_active[item] = self.active[item]
                del self.active[item]
        #print('freeze to', repr(self))

    def add(self, card, num):
        self.strip_dead(card-1)
        slices = to_slice(num)
        results = []
        for ptn in slices:
            single_items = [item for item in ptn if item == 1]
            multi_items = [item for item in ptn if item != 1]
            to_add_num = len(single_items)
            new_non_active = copy.deepcopy(self.non_active)
            for n in multi_items:
                k = (card,) * n
                if k not in new_non_active:
                    new_non_active[k] = 0
                new_non_active[k] += 1
            for x in multi_append(self.active, card, to_add_num):
                new_item = ActiveSet()
                new_item.active = x
                new_item.non_active = copy.deepcopy(new_non_active)
                new_item.parent = self
                new_item.freeze()
                new_item.strip_dead(card)
                results.append(new_item)
        return results


class ActiveSets:  # single color
    def __init__(self):
        self.cur = [ActiveSet()]

    #@verbose_f
    def add(self, card, num):
        new_cur = []
        for item in self.cur:
            new_cur += item.add(card, num)
        self.cur = new_cur

    def __repr__(self):
        return 'ActiveSets\n\t' + '\n\t'.join(map(repr, self.cur))

    def max3(self):
        return self.get_gram_stat()[0][0]

    def from_list(self, l):
        count = defaultdict(int)
        for item in l:
            count[item] += 1
        for k, v in sorted(count.items()):
            self.add(k, v)

    def get_gram_stat(self):
        result = set()
        for item in self.cur:
            two_count = 0
            three_count = 0
            for k, v in item.non_active.items():
                if len(k) == 2:
                    two_count += v
                elif len(k) == 3:
                    three_count += v
                else:
                    assert False, 'wtf' + repr(item)
            result.add((three_count, two_count))
        return vec_strip(result)


def vec_strip(x):
    s = sorted(x, reverse=True)
    result = [s[0]]
    for item in s[1:]:
        skip = False
        for c in result:
            if c[0] >= item[0] and c[1] >= item[1]:
                skip = True
                break
        if not skip:
            result.append(item)
    return result


class Seq:
    def __init__(self, start, length):
        self.start = start
        self.length = length


def color_stat(l):
    sets = ActiveSets()
    sets.from_list(l)
    return sets.get_gram_stat()


def assert_same(x):
    assert len(count(x).keys()) == 1, str(x) + ' should have only one type'


def join_list(xs, ys, f=operator.add):
    return [f(x, y) for x in xs for y in ys]


def to_slice(i, max_len=3):
    if i == 0:
        return [[]]
    result = []
    for l in range(1, min(max_len, i)+1):
        result += [[l] + item for item in to_slice(i-l,l)]
    return result


def handle_single(n):
    if n == 1:
        return [(0,0)]
    if n == 2:
        return [(0,1)]
    if n == 3:
        return [(1,0),(0,1)]
    if n == 4:
        return [(1,0),(0,2)]


def pair_adder(x, y):
    return x[0]+y[0], x[1]+y[1]


def handle_singles(l):
    c = count(l)
    seed = [(0,0)]
    for k, v in c.items():
        seed = vec_strip(join_list(seed, handle_single(v), pair_adder))
    return seed


def max_unit(cards):
    colors = [[] for _ in range(3)]
    singles = []
    for item in sorted(cards):
        if item//10 < 3:
            colors[item//10].append(item)
        else:
            singles.append(item)
    result = [(0,0)]
    for item in colors:
        result = vec_strip(join_list(result, color_stat(item), pair_adder))
    result = vec_strip(join_list(result, handle_singles(singles), pair_adder))
    return result


def eval_stat(p):
    two_coef = 0.99
    two_coef = 0.6
    #two_coef = 1.00
    return p[0] + two_coef * (min(p[1], 1))


def eval_naive(cards):
    return sorted(map(eval_stat, max_unit(cards)), reverse=True)[0]


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


def delta_prob(cards):
    delta = count(list_sub(all_cards(), cards))
    s = sum(delta.values())
    #print('sum is', s, 'cards', cards, 'delta', delta)
    for k in delta:
        delta[k] /= s
    return delta


def eval_rec(cards, f, verbose=False):
    if verbose:
        print('所有牌')
        print(display_cards(cards))
    prob = delta_prob(cards)
    base_metric = eval_naive(cards)
    final_metric = 0
    for k in prob:
        metric = f(cards + [k])
        final_metric += prob[k] * metric
        if verbose:
            print('摸牌:', card_to_str(k), '概率', prob[k], '得分', '%.2f'%base_metric,'+', '%.2f'%(metric-base_metric))
    if verbose:
        print('最终指标', final_metric)
    return final_metric

def eval1(cards):
    return eval_rec(cards, eval_naive)

def eval2(cards):
    return eval_rec(cards, eval1)


def select14(cards, metric_f=eval_naive):
    best = []
    handled = set()
    #eps = 1e-6
    for idx in range(len(cards)):
        if cards[idx] in handled:
            continue
        handled.add(cards[idx])
        cards_clone = cards[:]
        del cards_clone[idx]
        metric = metric_f(cards_clone)
        best.append((metric, cards[idx]))
    '''
        if len(best) == 0 or metric > best[0][0] + eps:
            best = [(metric, idx)]
        elif metric > best[0][0] - eps:
            best.append((metric, idx))
    '''
    #return sorted(list(set([cards[idx] for _, idx in best])))
    return sorted(best, reverse=True)


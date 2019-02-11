from collections import defaultdict
import random


wan1 = 1
wan2 = 2
wan3 = 3
wan4 = 4
wan5 = 5
wan6 = 6
wan7 = 7
wan8 = 8
wan9 = 9

suo1 = 11
suo2 = 12
suo3 = 13
suo4 = 14
suo5 = 15
suo6 = 16
suo7 = 17
suo8 = 18
suo9 = 19

tong1 = 21
tong2 = 22
tong3 = 23
tong4 = 24
tong5 = 25
tong6 = 26
tong7 = 27
tong8 = 28
tong9 = 29

east = 31
west = 32
south = 33
north = 34
center = 35
blank = 36
facai = 37


def all_tiles():
    result = list(range(1,10)) + list(range(11,20)) + list(range(21,30)) + list(range(31,38))
    result *= 4
    return sorted(result)


def split_by_category(x, count=False):
    sorted_x = sorted(x)
    result = [[], [], [], []]
    for item in sorted_x:
        result[item//10].append(item)
    return result


def tile_to_str(i):
    single = ['东风','西风','南风','北风','红中','白板','发财']
    color = ['万', '条', '筒']
    num = list('一二三四五六七八九')
    if i < 30:
        return num[i%10-1] + color[i//10]
    else:
        return single[i-31]


def display_tiles(tiles, newline=True):
    category = split_by_category(tiles)
    result_str = ''
    for c in category:
        result_str += ','.join(map(tile_to_str, c))
        if len(c) != 0:
            result_str += '\n' if newline else ' '
    result_str = result_str.rstrip()
    return result_str


def rand_tile():
    invalid_set = set([10,20,30])
    candidate = random.randrange(1,38)
    while candidate in invalid_set:
        candidate = random.randrange(1,38)
    return candidate


def rand_tile_no_single():
    invalid_set = set([10,20,30])
    candidate = random.randrange(1,30)
    while candidate in invalid_set:
        candidate = random.randrange(1,30)
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
    return [rand_tile() for _ in range(l)]


def rand_seq_no_single(l=13):
    return [rand_tile_no_single() for _ in range(l)]

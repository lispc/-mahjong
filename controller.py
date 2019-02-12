import random
import tile
import tile_pool
import agent


def round():
    p = tile_pool.Pool()
    agents = [agent.Agent("user%d"%idx) for idx in range(4)]
    for a in agents:
        a.init_tiles(p.next_n(13))

    next_tile = p.next()
    user_idx = 0
    while next_tile is not None:
        user = agents[user_idx]
        user.print()
        ok = user.add(next_tile)
        if ok:
            print('自摸:', user.name)
            user.print()
            return
        put_tile = user.next()
        msg = agent.Message(user.name, 'put', put_tile)
        for i in range(1,4):
            other = agents[(user_idx+i)%len(agents)]
            result = other.handle_msg(msg)
            if result.type == 'i_win':
                print('和牌:', other.name)
                other.print()
                return
        print()

        user_idx = (user_idx + 1)%len(agents)
        next_tile = p.next()

    print('平局')


def main():
    round()


if __name__ == '__main__':
    main()
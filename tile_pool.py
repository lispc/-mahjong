import random
import tile


class Pool:
    def __init__(self):
        self.tiles = tile.all_tiles()
        random.shuffle(self.tiles)
        self.idx = 0

    def next(self):
        if self.idx >= len(self.tiles):
            return None
        item = self.tiles[self.idx]
        self.idx += 1
        return item

    def next_n(self, n=14):
        result = self.tiles[self.idx:(self.idx+n)]
        assert len(result) == n
        self.idx += n
        return result

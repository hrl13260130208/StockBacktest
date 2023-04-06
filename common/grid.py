
from common.option import Option


class Grid():
    def __init__(self):
        self.min_grid = 500
        self.max_grid = 600
        self.step = 5
        self.num = 2000

        self.buy_grid = {}
        for g in range(self.min_grid, self.max_grid, self.step):
            self.add_buy(g)
        self.sell_grid = {}

    def del_buy(self, grid):
        del self.buy_grid[grid]

    def add_buy(self, grid):
        opt = Option()
        opt.grid = grid
        opt.num = self.num
        opt.option_type = 1
        opt.source = 3
        opt.source_object = self

        self.buy_grid[grid] = opt
        return opt

    def add_sell(self, grid, buy_options):
        opt = Option()
        opt.grid = grid
        opt.num = self.num
        opt.option_type = 2
        opt.source = 3
        opt.source_object = self
        opt.pair_option = buy_options

        self.sell_grid[grid] = opt
        return opt

    def del_sell(self, grid):
        del self.sell_grid[grid]
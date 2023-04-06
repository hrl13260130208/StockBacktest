from common.config import Config
from observer import Observer
from stock import StrategyManager, StockManager, Logs
from strategy.roll_strategy import RollStrategy
from strategy.open_strategy import OpenStrategy
from strategy.grid_strategy import GridStrategy
from strategy.region_strategy import RegionStrategy
# from strategy.multiple_strategy import MultipleStrategy
import requests
import json


class BackTest():

    def __init__(self):
        self.logs = Logs()
        self.config = Config()
        self.manager = StockManager(self.logs, self.config)
        # strategy=RollStrategy(self.manager)
        # strategy=RegionStrategy(self.manager)

        open_manager = StrategyManager(1, self.config, "open")
        self.manager.register_manager(open_manager.name , open_manager)
        open = OpenStrategy(open_manager, self.logs, self.config)

        grid_manager = StrategyManager(2, self.config, "grid")
        self.manager.register_manager(grid_manager.name, grid_manager)
        grid = GridStrategy(grid_manager, self.logs, self.config)
        # self.strategy=MultipleStrategy(self.manager)

        self.obs = Observer()
        self.obs.add_strategy(open)
        self.obs.add_strategy(grid)

    def run(self, start_date="20220607", end_date="20230220"):
        # 时间为key的净值，收益和同期沪深基准

        days = requests.get(f"http://localhost:5000/opendays?start={start_date}&end={end_date}")
        days = json.loads(days.text)
        for d in days:
            self.obs.run(d)

        self.obs.finish()
        self.manager.print_logs(days, print_detail=False)


if __name__ == '__main__':
    bt = BackTest()
    bt.run()

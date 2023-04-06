
from  observer import Observer
from stock import StrategyManager,StockManager,Logs
from strategy.roll_strategy import RollStrategy
from strategy.open_strategy import OpenStrategy
from strategy.grid_strategy import GridStrategy
from strategy.region_strategy import RegionStrategy
# from strategy.multiple_strategy import MultipleStrategy
import requests
import json


class BackTest():

    def __init__(self):
        self.logs=Logs()
        self.manager = StockManager(self.logs)
        # strategy=RollStrategy(self.manager)
        # strategy=RegionStrategy(self.manager)

        open_manager=StrategyManager(self.logs)
        self.manager.register_manager("open",open_manager)
        open=OpenStrategy(open_manager,logs=self.logs)

        grid_manager = StrategyManager(self.logs)
        self.manager.register_manager("grid", grid_manager)
        grid=GridStrategy(grid_manager,logs=self.logs)
        # self.strategy=MultipleStrategy(self.manager)

        self.obs=Observer()
        self.obs.add_strategy(open)
        # self.obs.add_strategy(grid)

    def run(self,start_date="20220607",end_date="20230220"):
        # 时间为key的净值，收益和同期沪深基准

        days=requests.get(f"http://localhost:5000/opendays?start={start_date}&end={end_date}")
        for d in json.loads(days.text):
            self.obs.run(d)

        self.obs.finish()
        self.manager.print_logs(print_detail=True)



if __name__ == '__main__':
    bt=BackTest()
    bt.run()
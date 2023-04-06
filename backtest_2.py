#
# import logging
# logging.basicConfig(level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger=logging.getLogger("BackTest_Multi")
#
# import pandas as pd
# from common import Config
# import matplotlib.pyplot as plt
# plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
#
# import strategy
# from data.dataset import CodeDataSet
# import utils
# import json
# import numpy as np
# from holding_code import HoldingCodes
#
#
#
# pd.set_option('display.max_columns', 1000)
# pd.set_option('display.width', 1000)
# pd.set_option('display.max_colwidth', 1000)
# pd.set_option('display.max_rows', None)
#
#
#
# def start(strategy,hold:HoldingCodes,db,start_date="20190101",end_date="20210910"):
#     # 时间为key的净值，收益和同期沪深基准
#     DF_PROFIT = pd.DataFrame(columns=["net_value", "profit", "hs300", "total"])
#     DF_ASSET = pd.DataFrame(columns=["total", "cash", "codes", "cash_percent"])
#
#
#     logger.info("开始回测...")
#     days = db.get_days(start_date,end_date)
#     # print(type(days),days)
#
#     last_date = None
#     hs300_start = 0
#
#     for d in days:
#
#         #   调整除权除息带来的影响
#         # holding_stock = Config.HOLDING_CODES.keys()
#         # if last_date != None and len(holding_stock) >0:
#         #     adjust_volume(Config.HOLDING_CODES)
#
#         # 处理待卖股票
#         hold.apply(d)
#
#         #   执行策略
#         strategy.run(date=d)
#
#         #   计算总资产
#         remain_cash,code_cash = hold.asset(d)
#
#         logger.info(f"回测日期：{d},当前资产：{remain_cash+code_cash},持有现金：{remain_cash},持股市值：{code_cash}")
#
#         hs300_value = db.hs300(d)[3]
#         if last_date == None:
#             hs300_start = hs300_value
#
#
#         utils.save_profit(DF_PROFIT,d,remain_cash+code_cash,hs300_value,hs300_start)
#         utils.save_asset(DF_ASSET,d,remain_cash,code_cash)
#
#         #   更新日期
#         last_date = d
#
#
#
#     mdd = compute_drawdown(DF_PROFIT)
#     compute_sharpe()
#
#     hc.markpoint()
#     hc.operate_txt()
#     print(f"最大回撤：{mdd}")
#
#     path= "data/backtest.json"
#     create_json(path,DF_PROFIT,DF_ASSET)
#
#
#
# def create_json(path,profit,asset):
#     '''
#         存储为json文件，用于echarts画图
#     :param path:
#     :param profit:
#     :param log:
#     :param kline:
#     :param macds:
#     :param rsi:
#     :return:
#     '''
#
#
#     d = {
#         "date": list(profit.index),
#         "net_value": list(profit["net_value"]),
#         "profit": list(profit["profit"]),
#         "hs300": list(profit["hs300"]),
#         "total": list(asset["total"]),
#         "cash": list(asset["cash"]),
#         "codes": list(asset["codes"]),
#         "cash_percent": list(asset["cash_percent"]),
#     }
#     s = json.dumps(d)
#     with open(path, "w+", encoding="utf-8") as f:
#         f.write(s)
#
#
#
# def adjust_volume(stocks):
#     """
#         调整除权除息带来的影响
#     :param stocks:
#     :return:
#     """
#     pass
#
#
#
# def compute_drawdown(profit):
#     # print(profit["total"].isnan())
#     return MaxDrawdown(profit["total"].values)
#
# def MaxDrawdown(return_list):
#
#     # 1. find all of the peak of cumlative return
#     maxcum = np.zeros(len(return_list))
#     b = return_list[0]
#     for i in range(0, len((return_list))):
#         if (return_list[i] > b):
#             b = return_list[i]
#         maxcum[i] = b
#
#     # 2. then find the max drawndown point
#     i = np.argmax((maxcum - return_list) / maxcum)
#     if i == 0:
#         return 0
#     j = np.argmax(return_list[:i])
#
#     # 3. return the maxdrawndown
#     return (return_list[j] - return_list[i]) / return_list[j]
#
# def compute_sharpe():
#     pass
#
#
#
#
# def grid():
#     conf = Config()
#     conf.SORT_BUY = False
#     db = CodeDataSet(conf)
#     hc = HoldingCodes(common=conf, cash=conf.INIT_CASH, db=db)
#
#     code = "601698.SH"
#     min = 13.84
#     max = 18.58
#     gs1 = strategy.GridStrategy(db, conf, hc, code, min=min, max=max, volume=200, auto_save=True)
#
#     # ts = startegy.CatboostStartegy(db,models.CatboostModel(conf,db),common=conf,holding_code=hc)
#     start(strategy=gs1, hold=hc, db=db, common=conf, start_date="20200930", end_date="20210930")
#
# if __name__ == '__main__':
#     conf = Config()
#     conf.SORT_BUY = False
#     conf.SKIP_CASH =False
#     db = CodeDataSet()
#     hc = HoldingCodes(common=conf, cash=conf.INIT_CASH, db=db)
#
#     # cm=models.CatboostModel(conf,db)
#     # lr_model=models.LRModel(conf,db)
#     # dense_model=models.DenseModel(conf,db)
#     # dense_model.predict("601698.SH","20211104")
#     # gs1 = strategy.SortStrategy(db, conf, hc,dense_model,stock_num=3)
#     code = "000069.SZ"
#     max = 12.4
#     min = 4.1
#     midpoint = 6.76
#     step=0.2
#     gs1 = strategy.GridStrategy(db, conf, hc, code, midpoint=midpoint,step=step,min=min, max=max)
#
#     #
#     # # ts = startegy.CatboostStartegy(db,models.CatboostModel(conf,db),common=conf,holding_code=hc)
#     start(strategy=gs1, hold=hc, db=db, common=conf, start_date="20200930", end_date="20210930")
#
#
#
#
#
#
#
#
#
#
#
#
#

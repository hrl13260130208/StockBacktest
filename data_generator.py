
import os
import json
from common.fields import TradeFieldWY,TradeFieldXL
import requests
def generate_file():
    prices={}

    d1=r"D:\data\webstock\trade_apply\wy"
    l1=os.listdir(d1)
    for i in l1:
        file = os.path.join(d1,i)
        date =i.replace(".txt","")
        p=[]
        with open(file,"r",encoding="utf-8") as f :
            for line in f.readlines():
                d=json.loads(line)
                if d[TradeFieldWY.CODE] == "000783":
                    p.append((d[TradeFieldWY.TIME],d[TradeFieldWY.CURRENT]))
        p = sorted(p, key=lambda x: x[0])
        prices[date] = p



    d2 = r"D:\data\webstock\trade_apply\wy"
    l2 = os.listdir(d2)
    for i in l2:
        file = os.path.join(d2, i)
        date = i.replace(".txt", "")
        p = []
        with open(file, "r", encoding="utf-8") as f:
            for line in f.readlines():
                d = json.loads(line)
                if d[TradeFieldXL.CODE] == "000783":
                    p.append((d[TradeFieldXL.TIME],d[TradeFieldXL.CURRENT]))
        p=sorted(p,key=lambda x:x[0])
        prices[date] = p


    with open("data/time_price_000783.json","w",encoding="utf-8") as f:
        json.dump(prices,f)

class TradePrice():

    def __init__(self):
        with open("data/time_price_000783.json", "r", encoding="utf-8") as f:
            self.prices = json.load(f)

    def trade_price(self,date):
        if date  in self.prices.keys():
            return self.prices[date]
        else:
            return None


    def check(self):
        k = self.prices.keys()

        k= sorted(k)
        start_date = "20220523"
        end_date = "20230220"
        days = requests.get(f"http://localhost:5000/opendays?start={start_date}&end={end_date}")

        d = json.loads(days.text)

        ki=0
        di=0
        less = 0
        while(ki<len(k) and di <len(d)):

            if (k[ki] == d[di]):
                print(d[di],k[ki])
                ki+=1
                di +=1
            else:
                less +=1
                print(d[di], "--------",less)
                di +=1

        print("-----------",less)
if __name__ == '__main__':
    generate_file()

    # tp=TradePrice()
    # tp.check()

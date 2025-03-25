from tabulate import tabulate
from ayaa.maket.data_mgr import DataMgr
from ayaa.strategy.strategy_mgr import StrategyMgr
from ayaa.trader.trader_a import TraderA
from ayaa.trader.trader_b import TraderB

if __name__ == '__main__':
    dmgr = DataMgr()
    smgr = StrategyMgr()
    trader = TraderA(dmgr, smgr)
    # trader = TraderB(dmgr, smgr)
    trader.set_profile("005827", 100000)
    targets = ["501010"]
    #targets = ["320007", "021225", "018421"]
    targets = ["004685", "017436", "005939", "501010", "501048", "161122", "320007", "018124", "005827"]
    res = []
    for i in targets:
        print(f'\nsymbol:{i}')
        # res.append(trader.auto_backtest(i, "2022-01-01", "2025-03-03"))
        res.append(trader.auto_backtest(i, "2022-01-01", "2025-03-03", visualize=True))

    filter = ['symbol', 'profit', 'amper', 'trade_times']
    fres =[{k:d[k] for k in filter} for d in res]
    print(tabulate(fres, headers="keys", tablefmt="grid"))
    # print(tabulate(res, headers=headers, tablefmt="grid"))

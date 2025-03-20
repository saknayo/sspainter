from ayaa.maket.data_mgr import DataMgr
from ayaa.strategy.strategy_mgr import StrategyMgr
from ayaa.trader.trader_a import TraderA

if __name__ == '__main__':
    dmgr = DataMgr()
    smgr = StrategyMgr()
    trader = TraderA(dmgr, smgr)
    trader.set_profile("005827", 100000)
    targets = ["004685", "017436", "005939", "501010", "501048", "161122", "320007", "018124", "005827"]
    for i in targets:
        print(f'\nsymbol:{i}')
        trader.auto_backtest(i, "2020-01-01", "2025-03-03")

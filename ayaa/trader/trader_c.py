from datetime import datetime
import pandas as pd
from typing import Dict, Any, Optional
from ayaa.strategy.finance_mgr import FinanceMgr

class TraderC:
    """
    交易员类 - 负责整合数据、策略和交易执行
    """
    
    def __init__(self, data_mgr: Any, strategy_mgr: Any):
        """
        初始化交易员
        :param data_mgr: 数据源管理器实例
        :param strategy_mgr: 策略管理器实例 
        """
        self.data_mgr = data_mgr
        self.strategy_mgr = strategy_mgr
        
        # 账户状态
        self.portfolio = {
            'cash': 1_000_000.0,  # 初始资金
            'positions': {},       # 持仓 {symbol: {'quantity': int, 'avg_price': float}}
            'history': []          # 交易历史记录
        }

    def set_profile(self, symbol, init_cash):
        self.symbol = symbol
        self.init_cash = init_cash

    def auto_backtest(self, spara, symbol, t_data, visualize = False):
        data = t_data.copy()
        # 获取数据
        upper = max(data['close'])
        lower = min(data['close'])
        amper = 100 * (data['close'].iloc[-1] - data['close'].iloc[0]) / data['close'].iloc[0]
        mpos = 1.0 * self.init_cash / lower
        
        # 初始化策略
        strategy = self.strategy_mgr.get_strategy('Grid')(spara)
        buy_fee = { 0 : 0.0015, 10000 : 0.001 }
        sell_fee = { 0 : 0.015, 7 : 0.005, 30 : 0}
        mgr_fee = 0
        fee_config = (buy_fee, sell_fee, mgr_fee)
        financer = FinanceMgr(init_cash=self.init_cash, buy_max_fee=0.001, sell_max_fee=0.000, max_holding_ration=spara['max_holding_ration'], fee_config=fee_config)
        strategy.set_financer(financer)

        # 执行回测
        strategy.backtest(symbol, data)
        trades, res = strategy.backtest_results()
        res['symbol'] = symbol 
        res['upper'] = upper
        res['lower'] = lower
        res['mpos'] = mpos
        res['amper'] = amper
        if visualize:
            strategy.visualize_strategy()
        return res
                   
if __name__ == "__main__":
    # 初始化依赖组件（需实现具体类）
    from ayaa.maket.data_mgr import DataMgr
    from ayaa.strategy.strategy_mgr import StrategyMgr
    
    data_mgr = DataMgr()
    strategy_mgr = StrategyMgr()
    
    # 创建交易员实例
    trader = TraderC(data_mgr, strategy_mgr)

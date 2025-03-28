from datetime import datetime
import pandas as pd
from typing import Dict, Any, Optional
from ayaa.strategy.finance_mgr import FinanceMgr

class TraderA:
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
        
        # 运行时状态
        self.current_data = None    # 当前市场数据
        self.selected_symbol = None # 当前交易标的
        '''self.active_strategy = self.strategy_mgr.get_strategy('Grid')(
            grid_num=10,
            lower_bound=1.5,
            upper_bound=2,
            order_percent=0.05,
            max_position=100000)
        '''
        self.active_strategy = self.strategy_mgr.get_strategy('Shan')(
            portion=0.5,
            linspace=0.05,
            lower_bound=25,
            upper_bound=35)

    def set_profile(self, symbol, init_cash):
        self.selected_symbol = symbol
        self.init_cash = init_cash

    def backtest(self):
        # 获取数据
        data = self.data_mgr.fetch_daily_stock_data('fund', self.selected_symbol, '2024-01-01', '2025-03-19')
        #data['close'] = data['nav']
        
        # 初始化策略
        # self.active_strategy.set_initial_state(initial_capital=self.init_cash, current_cash=self.init_cash, current_holdings=0)

        # 执行回测
        self.active_strategy.backtest(data)
        trades, res = self.active_strategy.backtest_results()
        self.active_strategy.visualize_strategy()
        
        # 输出交易记录
        print("\n前5笔交易记录：")
        #print(trades.head())
        print(trades)
 
    def auto_backtest(self, symbol, start_date, end_date, visualize = False):
        spara = {
            # financer
            'max_holding_ration' : 0.8,
            # strategy
            'grid_num' : 10,
            'order_percent' : 0.05,
            'window' : 60,
            'num_std' : 5,
            'sbc5' : 1,
        }
        # 获取数据
        data = self.data_mgr.fetch_daily_stock_data('fund', symbol, start_date, end_date)
        data['close'] = data['nav']
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
    trader = Trader(data_mgr, strategy_mgr)

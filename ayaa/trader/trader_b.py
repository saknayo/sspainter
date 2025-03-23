from datetime import datetime
import pandas as pd
from typing import Dict, Any, Optional

class TraderB:
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
        self.active_strategy = self.strategy_mgr.get_strategy('Shan')(
            portion=0.2,
            linspace=0.02,
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
        self.active_strategy.set_initial_state(initial_capital=self.init_cash, current_cash=self.init_cash, current_holdings=0)

        # 执行回测
        self.active_strategy.backtest(data)
        trades = self.active_strategy.backtest_results()
        self.active_strategy.visualize_strategy()
        
        # 输出交易记录
        print("\n前5笔交易记录：")
        #print(trades.head())
        print(trades)
 
    def auto_backtest(self, symbol, start_date, end_date):
        # 获取数据
        data = self.data_mgr.fetch_daily_stock_data('fund', symbol, start_date, end_date)

        # 初始化策略
        strategy = self.active_strategy
        strategy.reset_state()
        strategy.set_initial_state(initial_capital=self.init_cash, current_cash=self.init_cash, current_holdings=0)

        # 执行回测
        strategy.backtest(data)
        trades = strategy.backtest_results()
        amper = (data['close'].iloc[-1] - data['close'].iloc[0]) / data['close'].iloc[0]
        print(f"涨跌幅:{amper*100:.2f}%")
        strategy.visualize_strategy()
                   
if __name__ == "__main__":
    # 初始化依赖组件（需实现具体类）
    from ayaa.maket.data_mgr import DataMgr
    from ayaa.strategy.strategy_mgr import StrategyMgr
    
    data_mgr = DataMgr()
    strategy_mgr = StrategyMgr()
    
    # 创建交易员实例
    trader = Trader(data_mgr, strategy_mgr)

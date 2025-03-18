
from datetime import datetime
import pandas as pd
from typing import Dict, Any, Optional

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
        self.active_strategy = None # 当前激活策略
        
    def load_historical_data(self, start: str, end: str) -> pd.DataFrame:
        """加载历史数据"""
        df = self.data_mgr.get_historical_data(
            symbol=self.selected_symbol, 
            start=datetime.fromisoformat(start),
            end=datetime.fromisoformat(end)
        )
        self.current_data = df
        return df

    def select_strategy(self, strategy_type: str, **params):
        """
        选择并初始化交易策略
        :param strategy_type: 策略类型 (e.g., 'momentum', 'mean_reversion')
        :param params: 策略参数
        """
        self.active_strategy = self.strategy_mgr.get_strategy(
            strategy_type, **params
        )
        print(f"策略已切换为 [{strategy_type}]，参数 {params}")

    def run_backtest(self) -> Dict[str, Any]:
        """
        执行回测
        :return: 回测结果指标
        """
        if self.current_data is None:
            raise ValueError("请先加载历史数据")
            
        # 初始化回测状态
        backtest_portfolio = self.portfolio.copy()
        backtest_portfolio['positions'] = {}
        data = self.current_data.copy()
        
        # 遍历历史数据
        for idx, row in data.iterrows():
            signal = self.active_strategy.generate_signal(row.to_dict())
            self._execute_signal(signal, backtest_portfolio, is_backtest=True)
        
        # 计算回测指标
        initial = self.portfolio['cash']
        final = backtest_portfolio['cash'] + sum(
            pos['quantity'] * data.iloc[-1]['close'] 
            for pos in backtest_portfolio['positions'].values()
        )
        return {
            'return_pct': (final - initial) / initial * 100,
            'max_drawdown': self._calculate_max_drawdown(data),
            'transactions': backtest_portfolio['history']
        }

    def start_real_trading(self):
        """启动实时交易"""
        def realtime_callback(data: dict):
            self.current_data = data
            signal = self.active_strategy.generate_signal(data)
            self._execute_signal(signal, self.portfolio)
            
        self.data_mgr.subscribe_real_time(
            symbol=self.selected_symbol,
            callback=realtime_callback
        )

    def _execute_signal(self, signal: dict, portfolio: dict, is_backtest=False):
        """
        执行交易信号（内部方法）
        :param signal: 交易信号 {'action': 'buy/sell', 'price': float, 'volume': int}
        :param portfolio: 要更新的账户组合
        :param is_backtest: 是否为回测模式
        """
        action = signal.get('action')
        symbol = self.selected_symbol
        price = signal['price']
        volume = signal['volume']
        
        if action == 'buy' and volume > 0:
            cost = price * volume
            if portfolio['cash'] >= cost:
                portfolio['cash'] -= cost
                if symbol not in portfolio['positions']:
                    portfolio['positions'][symbol] = {'quantity': 0, 'avg_price': 0.0}
                pos = portfolio['positions'][symbol]
                new_qty = pos['quantity'] + volume
                pos['avg_price'] = (pos['avg_price'] * pos['quantity'] + cost) / new_qty
                pos['quantity'] = new_qty
                self._record_transaction(signal, portfolio, is_backtest)
                
        elif action == 'sell' and volume > 0:
            if symbol in portfolio['positions']:
                pos = portfolio['positions'][symbol]
                if pos['quantity'] >= volume:
                    proceeds = price * volume
                    portfolio['cash'] += proceeds
                    pos['quantity'] -= volume
                    if pos['quantity'] == 0:
                        del portfolio['positions'][symbol]
                    self._record_transaction(signal, portfolio, is_backtest)

    def _record_transaction(self, signal: dict, portfolio: dict, is_backtest: bool):
        """记录交易日志"""
        log = {
            'time': datetime.now().isoformat() if not is_backtest else signal['time'],
            'symbol': self.selected_symbol,
            'action': signal['action'],
            'price': signal['price'],
            'volume': signal['volume'],
            'cash': portfolio['cash'],
            'positions': portfolio['positions'].copy()
        }
        portfolio['history'].append(log)

    def _calculate_max_drawdown(self, data: pd.DataFrame) -> float:
        """计算最大回撤（示例实现）"""
        peaks = data['close'].cummax()
        drawdowns = (data['close'] - peaks) / peaks
        return drawdowns.min() * 100

# 使用示例
if __name__ == "__main__":
    # 初始化依赖组件（需实现具体类）
    from data_manager import DataManager
    from strategy_manager import StrategyManager
    
    data_mgr = DataManager()
    strategy_mgr = StrategyManager()
    
    # 创建交易员实例
    trader = Trader(data_mgr, strategy_mgr)
    
    # 配置数据源和策略
    trader.select_data_source('stock', 'AAPL')
    trader.load_historical_data('2022-01-01', '2023-01-01')
    trader.select_strategy('momentum', window=20, threshold=0.05)
    
    # 执行回测
    backtest_result = trader.run_backtest()
    print(f"回测收益: {backtest_result['return_pct']:.2f}%")
    
    # 启动实盘交易
    trader.start_real_trading()

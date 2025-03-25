import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ayaa.strategy.finance_mgr import FinanceMgr
from ayaa.utils.perf import calculate_bollinger_bands

class GridTradingStrategy:
    def __init__(self,
        grid_num=15,
        lower_bound=25,
        upper_bound=35,
        order_percent=0.08,
        max_position=1000):
        """
        网格交易策略
        """
        self.data = None
        self.positions = []  # 记录所有交易
        self.holding_rations = []  # 当前持有数量
        
        # 策略参数
        self.grid_params = {
            'grid_num': grid_num,        # 网格数量
            'lower_bound': lower_bound,   # 价格下限
            'upper_bound': upper_bound,   # 价格上限
            'order_percent': order_percent,  # 每格交易资金比例
            'max_position': max_position # 最大持仓限制
        }
        
        # 生成网格区间
        self.generate_grid_levels()
        self.last_grid = 0
        self.last_trade_time = 0
   
    def set_financer(self, financer):
        self.financer = financer

    def reset_state(self):
        self.positions = []  # clear trade records
        self.holding_rations = []
        self.data = None
        self.financer.reset()

    def generate_grid_levels(self):
        """生成网格价格区间"""
        price_range = np.linspace(
            self.grid_params['lower_bound'],
            self.grid_params['upper_bound'],
            self.grid_params['grid_num'] + 1
        )
        self.grid_levels = price_range.tolist()
        #print(f"生成网格价格区间：{self.grid_levels}")

    def reset_grid_level(self, lower, upper, grid_num=None):
        self.grid_params['lower_bound'] = lower
        self.grid_params['upper_bound'] = upper
        self.grid_params['grid_num'] = grid_num if grid_num else self.grid_params['grid_num'] 
        self.generate_grid_levels()
        
    
    def calculate_order_size(self, price):
        """计算单次交易数量"""
        return (self.financer.init_cash * self.grid_params['order_percent']) / price

    def execute_strategy(self, current_date, current_price):
        """执行策略"""
        quantity = 0
        current_grid = np.digitize(current_price, self.grid_levels)
        self.last_trade_time += 1
        
        if current_grid != self.last_grid:
            self.last_grid = current_grid
            self.last_trade_time = 0

            # 检查每个网格线
            for level in self.grid_levels:
                # 买入条件：价格低于网格线且未持仓
                if current_price <= level:
                    order_qty = self.calculate_order_size(current_price)
                    quantity += order_qty
                # 卖出条件：价格高于网格线且有持仓
                if current_price >= level:
                    order_qty = self.calculate_order_size(current_price)
                    quantity -= order_qty

        real_quantity = 0
        stype = ''
        if quantity > 1:
            real_quantity = self.financer.buy(current_date, current_price, abs(quantity))
            stype = 'BUY'
        if quantity < -1:
            real_quantity = self.financer.sell(current_date, current_price, abs(quantity))
            stype = 'SELL'
        if real_quantity > 1:
            # print(f'date : {current_date} price : {current_price} quantity  : {real_quantity} type  : {stype}')
            self.positions.append({
                'date': current_date,
                'price': current_price,
                'quantity' : real_quantity,
                'type' : stype,
            })
 
    '''def execute_strategy(self, current_date, current_price):
        """执行策略"""
        quantity = 0
        
        # 检查每个网格线
        for level in self.grid_levels:
            # 买入条件：价格低于网格线且未持仓
            if current_price <= level:
                order_qty = self.calculate_order_size(current_price)
                quantity += order_qty
            # 卖出条件：价格高于网格线且有持仓
            if current_price >= level:
                order_qty = self.calculate_order_size(current_price)
                quantity -= order_qty

        real_quantity = 0
        stype = ''
        if quantity > 1:
            real_quantity = self.financer.buy(current_date, current_price, abs(quantity))
            stype = 'BUY'
        if quantity < -1:
            real_quantity = self.financer.sell(current_date, current_price, abs(quantity))
            stype = 'SELL'
        if real_quantity > 1:
            # print(f'date : {current_date} price : {current_price} quantity  : {real_quantity} type  : {stype}')
            self.positions.append({
                'date': current_date,
                'price': current_price,
                'quantity' : real_quantity,
                'type' : stype,
            })'''
    def backtest(self, symbol, data):
        self.symbol = symbol
        self.data = data
        self.ub = calculate_bollinger_bands(data, window=60, num_std=5, price_col='close', fill_na=True)
        for idx, row in data.iterrows():
            self.reset_grid_level(self.ub.iloc[idx]['lower_band'], self.ub.iloc[idx]['upper_band']) 
            self.execute_strategy(row['date'], row['close'])
            self.holding_rations.append({'date':row['date'],
                                         'ration':self.financer.get_holding_ration(row['close']),
                                         'profit':self.financer.get_profit(row['close']) })

    def backtest_results(self, printf = False):
        """回测结果分析"""
        # 计算最终资产
        final_value = self.financer.get_total_value(self.data['close'].iloc[-1])
        total_return = self.financer.get_profit(self.data['close'].iloc[-1])
        
        # 统计交易数据
        trades = pd.DataFrame(self.positions)
        win_trades = trades[trades['type'] == 'SELL']

        if printf: 
            print("\n========== 回测结果 ==========")
            print(f"初始资金: {self.financer.init_cash:.2f}")
            print(f"最终资产: {final_value:.2f}")
            print(f"总收益率: {total_return*100:.2f}%")
            print(f"最终持仓: {self.financer.total_holding:.2f}")
            print(f"总交易次数: {len(trades)}/{len(self.data)}")
            print(f"买卖比例: {len(win_trades)/len(trades):.2%}")
            print(f"sprice: {self.data['close'].iloc[0]}")
            print(f"eprice: {self.data['close'].iloc[-1]}")
  
        res = {
            "init_cash" : self.financer.init_cash,
            "final_cash" : final_value,
            "profit" : total_return*100,
            "holding" : self.financer.total_holding,
            "trade_times" : f'{len(trades)}/{len(self.data)}',
            "sell_buy" : len(win_trades)/len(trades),
            "sprice" : self.data['close'].iloc[0],
            "eprice" : self.data['close'].iloc[-1],
        }
  
        return trades, res
    
    def visualize_strategy(self):
        """可视化策略执行"""
        plt.figure(figsize=(24,12))
        plt.plot(self.data['date'], self.data['close'], label='Price')
        plt.plot(self.data['date'], self.ub['lower_band'], label='Lower')
        plt.plot(self.data['date'], self.ub['upper_band'], label='Upper')
        plt.plot(self.data['date'], self.ub['sda'], label='sda')
        plt.plot(self.data['date'], self.ub['sma'], label='sma')
        plt.plot([i['date'] for i in self.holding_rations], [i['ration'] for i in self.holding_rations], label='Holding Ration')
        plt.plot([i['date'] for i in self.holding_rations], [i['profit'] for i in self.holding_rations], label='Profit')
        plt.axhline(y=0, color="black", linestyle=":")
        plt.axhline(y=1, color="black", linestyle=":")
        
        # 绘制买卖点
        buys = [t for t in self.positions if t['type'] == 'BUY']
        sells = [t for t in self.positions if t['type'] == 'SELL']
        
        plt.scatter(
            [b['date'] for b in buys],
            [b['price'] for b in buys],
            color='green', marker='^', label='Buy'
        )
        plt.scatter(
            [s['date'] for s in sells],
            [s['price'] for s in sells],
            color='red', marker='v', label='Sell'
        )
        
        # 绘制网格线
        for level in self.grid_levels:
            plt.axhline(y=level, color='gray', linestyle='--', alpha=0.5)
            
        plt.title('Grid Trading Strategy')
        plt.legend()
        plt.savefig(f'misc/{self.symbol}.jpg', dpi = 100)
        # plt.show()

# 使用示例
if __name__ == "__main__":
    # 加载示例数据（需替换为真实数据）
    # 设置随机种子（确保结果可重复）
    #np.random.seed(0)
    # 生成日期（假设从2023-10-01开始）
    length = 200
    dates = pd.date_range(start="2023-10-01", periods=length)
    # 生成价格数据（模拟股价波动）
    base_price = 30.0  # 初始价格
    #price_changes = np.random.normal(0, 0.051, length) + 1  # 正态分布随机波动（均值为0，标准差为2）
    #price = np.round(base_price * price_changes.cumprod(), 2)  # 累积波动并保留两位小数
    price_changes = np.random.randn(200) * 2  # 正态分布随机波动（均值为0，标准差为2）
    price = np.round(base_price + price_changes.cumsum(), 2)  # 累积波动并保留两位小数
    # 创建DataFrame
    data = pd.DataFrame({
        "date": dates,
        "close": price
    })
    print(data)

    #data = pd.read_csv('stock_data.csv', index_col='date', parse_dates=True)
    
    # 初始化策略
    strategy = GridTradingStrategy(grid_num=10, lower_bound=25, upper_bound=35, order_percent=0.08, max_position=10000)
    buy_fee = { 0 : 0.0015, 10000 : 0.001 }
    sell_fee = { 0 : 0.015, 7 : 0.005, 30 : 0}
    mgr_fee = 0
    fee_config = (buy_fee, sell_fee, mgr_fee)
    financer = FinanceMgr(init_cash=100000, buy_max_fee=0.001, sell_max_fee=0.000, max_holding_ration=0.8, fee_config=fee_config)
    strategy.set_financer(financer)
    # 执行回测
    strategy.backtest(data)
    trades, res = strategy.backtest_results()
    strategy.visualize_strategy()
    
    # 输出交易记录
    print("\n前5笔交易记录：")
    #print(trades.head())
    print(trades)

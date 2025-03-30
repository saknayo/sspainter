from tabulate import tabulate
import optuna
from typing import Dict, Any
from functools import lru_cache
import numpy as np
from ayaa.maket.data_mgr import DataMgr
from ayaa.strategy.strategy_mgr import StrategyMgr
from ayaa.trader.trader_a import TraderA
from ayaa.trader.trader_c import TraderC

@lru_cache(maxsize=10)
def get_fund_rank_list(select_num):
    import akshare as ak
    fund_open_fund_rank_em_df = ak.fund_open_fund_rank_em(symbol="全部")
    # print(fund_open_fund_rank_em_df)
    # print(fund_open_fund_rank_em_df['基金代码'])
    return fund_open_fund_rank_em_df['基金代码'][np.random.choice(len(fund_open_fund_rank_em_df), select_num)]


def generate_test_batch(data, length, batch_num):
    if len(data) < length:
        return []
    test_datas = []
    for i in np.random.choice(len(data) - length, min(len(data) - length, batch_num)):
        test_datas.append(data[i:i+length])
    return test_datas

def collect_data(dm, symbols, start_date, end_date):
    for syb in symbols:
        dm.fetch_daily_stock_data('fund', syb, start_date, end_date)

def stats(res, period):
    ''' 按照涨跌幅大于5% 小于-5%，以及介于两者之间分三类统计，并计算平均盈利率 '''
    # seperate by holding time
    stats_res ={'>5%':[], '<-5%':[], '-5%-5%':[], 'total':[]}
    for r in res:
        if r['amper'] > 5 :
            stats_res['>5%'].append(r['diff'])
        elif r['amper'] < -5 :
            stats_res['<-5%'].append(r['diff'])
        else:
            stats_res['-5%-5%'].append(r['diff'])
        stats_res['total'].append(r['diff'])
    finnal = [{'name':k, 'avg':np.mean(s), 'num':len(s)} for k, s in stats_res.items()]
    print(tabulate(finnal, headers="keys", tablefmt="grid"))
    #return np.mean([finnal[0]['avg'], finnal[1]['avg'], finnal[2]['avg']])
    return finnal[-1]['avg']

def evalution(spara):
    init_cash = 100000

    dmgr = DataMgr()
    smgr = StrategyMgr()
    trader = TraderC(dmgr, smgr)

    res = []
    symbol_num = 10
    length = 360
    batch_num = 1

    # symbol_list = get_fund_rank_list(symbol_num)
    symbol_list = ["004685", "017436", "005939", "501010", "501048", "161122", "320007", "018124", "005827", '270042']
    #collect_data(dmgr, symbol_list, "2001-01-01", "2025-03-03")
    #exit(0)
    for symbol in symbol_list:
        data = dmgr.fetch_all_daily_stock_data('fund', symbol)
        batches = generate_test_batch(data, length, batch_num)
        trader.set_profile(symbol, init_cash)
        for batch_data in batches:
            # print(batch_data)
            res.append(trader.auto_backtest(spara, symbol, batch_data, visualize=True))

    [r.update({'diff':r['profit']-r['amper']}) for r in res]
    filter = ['symbol', 'diff', 'profit', 'amper', 'trade_times']
    fres =[{k:d[k] for k in filter} for d in res]
    print(tabulate(fres, headers="keys", tablefmt="grid"))
    return stats(res, length) / 100

if __name__ == '__main__':
    np.random.seed(0)
    spara = {
        # financer
        'max_holding_ration' : 0.8,
        # strategy
        'grid_num' : 10,
        'order_percent' : 0.05,
        'window' : 60,
        'num_std' : 5,
        'sbc5' : 1,
        'min_width' : 0.2,
        'max_width' : 0.4,
    }
    spara = {'max_holding_ration': 0.8, 'order_percent': 0.16906228159872866, 'u_num_std': 0.20060052911467804, 'l_num_std': 6.8878886392475005, 
    'u_sbc5': 1.775046498978191, 'l_sbc5': 7.278347871528191, 'max_width': 0.7997296468545225, 'min_width': 0.15540867980513814, 'grid_num': 15, 'window': 81}
    # r3-total_avg-num_std-sbc
    # [I 2025-03-30 18:29:31,058] Trial 93 finished with value: 3.936108227230945 and parameters: 
    spara = {'max_holding_ration': 0.8, 'order_percent': 0.1377678930628302, 'u_num_std': 2.257133984723932, 'l_num_std': 8.823753694502832, 
     'u_sbc5': 0.5477913042862884, 'l_sbc5': 6.200430538876671, 'max_width': 0.1, 'min_width': 0.1, 'grid_num': 10, 'window': 60}

    # 执行优化
    evalution(spara)


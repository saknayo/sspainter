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
    return finnal[2]['avg']

def evalution(spara):
    init_cash = 100000

    dmgr = DataMgr()
    smgr = StrategyMgr()
    trader = TraderC(dmgr, smgr)

    res = []
    symbol_num = 100
    length = 360
    batch_num = 30

    symbol_list = get_fund_rank_list(symbol_num)
    #collect_data(dmgr, symbol_list, "2001-01-01", "2025-03-03")
    #exit(0)
    for symbol in symbol_list:
        data = dmgr.fetch_all_daily_stock_data('fund', symbol)
        batches = generate_test_batch(data, length, batch_num)
        trader.set_profile(symbol, init_cash)
        for batch_data in batches:
            # print(batch_data)
            res.append(trader.auto_backtest(spara, symbol, batch_data, visualize=False))

    [r.update({'diff':r['profit']-r['amper']}) for r in res]
    filter = ['symbol', 'diff', 'profit', 'amper', 'trade_times']
    fres =[{k:d[k] for k in filter} for d in res]
    #print(tabulate(fres, headers="keys", tablefmt="grid"))
    return stats(res, length) / 100


def create_objective(eval_func, param_space: Dict[str, Any]):
    """动态创建Optuna目标函数"""
    def objective(trial):
        params = {}
        for name, config in param_space.items():
            if config['type'] == 'float':
                params[name] = trial.suggest_float(
                    name,
                    config['low'],
                    config['high'],
                    log=config.get('log', False)
                )
            elif config['type'] == 'int':
                params[name] = trial.suggest_int(
                    name,
                    config['low'],
                    config['high']
                )
            elif config['type'] == 'categorical':
                params[name] = trial.suggest_categorical(
                    name,
                    config['options']
                )
        return eval_func(params)
    return objective

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
    #evalution(spara)
    # 用户自定义参数空间（示例）
    HYPERPARAM_SPACE = {
        'max_holding_ration': {
            'type': 'float',
            'low': 0.8,
            'high': 0.8,
            'log': True  # 对数尺度采样
        },
        'order_percent': {
            'type': 'float',
            'low': 0.03,
            'high': 0.20,
            'log': True  # 对数尺度采样
        },
        'u_num_std': {
            'type': 'float',
            'low': 0.2,
            'high': 10,
            'log': True  # 对数尺度采样
        },
        'l_num_std': {
            'type': 'float',
            'low': 0.2,
            'high': 10,
            'log': True  # 对数尺度采样
        },
        'u_sbc5': {
            'type': 'float',
            'low': 0.1,
            'high': 10,
            'log': True  # 对数尺度采样
        },
        'l_sbc5': {
            'type': 'float',
            'low': 0.1,
            'high': 10,
            'log': True  # 对数尺度采样
        },
        'max_width': {
            'type': 'float',
            'low': 0.1,
            'high': 1.0,
            'log': True  # 对数尺度采样
        },
        'min_width': {
            'type': 'float',
            'low': 0.1,
            'high': 1.0,
            'log': True  # 对数尺度采样
        },
        'grid_num': {
            'type': 'int',
            'low': 3,
            'high': 15
        },
        'window': {
            'type': 'int',
            'low': 5,
            'high': 90
        },
    }



    # 执行优化
    study = optuna.create_study(direction='maximize')
    objective = create_objective(evalution, HYPERPARAM_SPACE)
    study.optimize(objective, n_trials=100)

    # 输出结果
    print(f"最佳参数: {study.best_params}")
    print(f"最佳得分: {study.best_value:.4f}")



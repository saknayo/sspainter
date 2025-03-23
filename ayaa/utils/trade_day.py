from datetime import date, timedelta
import pandas as pd
import akshare as ak
from functools import lru_cache

# 获取全量交易日历数据
@lru_cache(maxsize=1)
def get_trading_days():
    # output : datetime.date list
    trade_dates_df = ak.tool_trade_date_hist_sina() # numpy.datetime64('1990-12-19T00:00:00.000000000')
    # 转换日期格式并过滤
    trade_dates_df['trade_date'] = pd.to_datetime(trade_dates_df['trade_date'])
    print('last', trade_dates_df.iloc[-1])
    return set(pd.Timestamp(t).to_pydatetime().date()  for t in trade_dates_df['trade_date'].values) 

@lru_cache(maxsize=100)
def is_trading_day(date):
    return date in get_trading_days()

def get_next_trading_day(t_date, delta_days=1):
    """计算顺延后的交易日（跳过节假日和周末）"""
    target_date = t_date + timedelta(days=delta_days)
    while not is_trading_day(target_date):
        target_date += timedelta(days=1)
    return target_date

def calc_hold_days(buy_t_date, sell_t_date, fund_type="Normal"):
    """
    优化版基金持有天数计算器
    :param buy_t_date:  申购成交日(T日，格式:YYYY-MM-DD)
    :param sell_t_date: 赎回成交日(T日，格式:YYYY-MM-DD)
    :param fund_type:  基金类型(普通/QDII/货币)
    :return: 包含确认日期、持有天数和费用提示的字典
    """
    # 转换日期格式
    buy_t = date.fromisoformat(buy_t_date) if isinstance(buy_t_date, str) else buy_t_date
    sell_t = date.fromisoformat(sell_t_date) if isinstance(sell_t_date, str) else sell_t_date
    
    # 计算确认日期偏移量（根据基金类型）
    delta_map = {"Normal":1, "Huobi":1, "QDII":2}
    buy_confirm = get_next_trading_day(buy_t, delta_map.get(fund_type,1))
    sell_confirm = get_next_trading_day(sell_t, delta_map.get(fund_type,1))

    # 有效性校验
    if sell_confirm < buy_confirm:
        raise ValueError("赎回日期不能早于申购日期")

    # 计算持有天数（自然日）
    return (sell_confirm - buy_confirm).days

if __name__ == "__main__":
    
    # 案例1：周四申购，周五赎回（遇节假日顺延）
    result = calc_hold_days(
        buy_t_date="2024-04-03",
        sell_t_date="2024-04-14",  # 周五赎回T日
    )
    print("【案例1】清明节前交易：", result)

    # 案例2：QDII基金处理
    result_qdii = calc_hold_days(
        buy_t_date="2025-03-17",
        sell_t_date="2025-03-19",
        fund_type="QDII"
    )
    print("\n【案例2】QDII基金：")
    print(f"确认日期差：{result_qdii}天")


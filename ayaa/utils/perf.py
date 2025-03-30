import pandas as pd
import talib
import numpy as np

def calculate_perf(data, window, price_col='close', fill_na=False):
    """
    计算布林通道
    参数：
    data: DataFrame - 包含价格数据的DataFrame
    price_col: str - 价格列名称（默认'close'）

    返回：
    包含原始数据和布林通道的DataFrame
    """
    df = data

    # 计算中轨（移动平均）
    df['sma'] = df[price_col].rolling(window=window).mean()
    df['sma5'] = df[price_col].rolling(window=5).mean()
    df['sbc5'] = 1*(df[price_col] - df['sma5'])
    df['sbc5p'] = df['sbc5'].apply(lambda x : x if x > 0 else 0)
    df['sbc5n'] = df['sbc5'].apply(lambda x : x if x < 0 else 0)

    df['rsi'] = talib.RSI(df[price_col], timeperiod=14) / 100
    df['macd'], df['signal'], df['hist'] = talib.MACD(df[price_col], fastperiod=12, slowperiod=26, signalperiod=9)
    # df['hist_diff'] = np.diff(df['hist'], prepend=df['hist'][0])
    # df['macd_diff'] = np.diff(df['macd'], prepend=df['macd'][0])
    df['macd_diff'] = np.diff(df['macd'], prepend=0)
    # 计算标准差
    df['sda'] = df[price_col].rolling(window=window).std()
    rolling_std = df[price_col].rolling(window=window).std()

    if fill_na:
        fill_d = pd.DataFrame({
            'upper_band': 1.2 * df[price_col],
            'lower_band': 0.8 * df[price_col],
        })
        df.fillna(fill_d, inplace=True)
    return df


def calculate_bollinger_bands(data, window=20, num_std=2, price_col='close', fill_na=False):
    """
    计算布林通道
    参数：
    data: DataFrame - 包含价格数据的DataFrame
    window: int - 移动平均窗口周期（默认20）
    num_std: int - 标准差倍数（默认2）
    price_col: str - 价格列名称（默认'close'）

    返回：
    包含原始数据和布林通道的DataFrame
    """
    df = data.copy()

    # 计算中轨（移动平均）
    df['sma'] = df[price_col].rolling(window=window).mean()
    df['sma5'] = df[price_col].rolling(window=5).mean()
    df['sbc5'] = 1*(df[price_col] - df['sma5'])
    df['sbc5p'] = df['sbc5'].apply(lambda x : x if x > 0 else 0)
    df['sbc5n'] = df['sbc5'].apply(lambda x : x if x < 0 else 0)

    df['rsi'] = talib.RSI(df[price_col], timeperiod=14) / 100
    df['macd'], df['signal'], df['hist'] = talib.MACD(df[price_col], fastperiod=12, slowperiod=26, signalperiod=9)
    df['hist_diff'] = np.diff(df['hist'], prepend=df['hist'][0])
    # 计算标准差
    df['sda'] = df[price_col].rolling(window=window).std()
    rolling_std = df[price_col].rolling(window=window).std()
    #rolling_std = 2*df[price_col].rolling(window=60).std()
   # rolling_std += df[price_col].rolling(window=5).std()

    df['min_width'] = df['sma'] * 0.2 / num_std
    df['max_width'] = df['sma'] * 0.4 / num_std
    #rolling_std = df[['min_width', 'sda']].max(axis=1)
    rolling_std = df[['max_width', 'sda']].min(axis=1)
    # 计算上下轨
    df['upper_band'] = df['sma'] + (rolling_std * num_std) + df['sbc5']
    df['lower_band'] = df['sma'] - (rolling_std * num_std) + df['sbc5']
    #df['max_sma'] = df['sma'] * 1.4
    #df['upper_band'] = df[['max_sma', 'upper_band']].min(axis=1)
    #df['lower_band'] = df[['min_sma', 'lower_band']].max(axis=1)

    #df['upper_band'] = (df['sma'] + (rolling_std * num_std))* (df['rsi'] / 0.7)
    #df['lower_band'] = (df['sma'] - (rolling_std * num_std))* (df['rsi'] / 0.3)

    if fill_na:
        fill_d = pd.DataFrame({
            'upper_band': 1.2 * df[price_col],
            'lower_band': 0.8 * df[price_col],
        })
        df.fillna(fill_d, inplace=True)
    return df

# 使用示例
if __name__ == "__main__":
    # 生成示例数据（假设每天收盘价）
    dates = pd.date_range(start='2023-01-01', periods=30)
    np.random.seed(0)
    prices = np.random.normal(100, 5, 30).cumsum()  # 随机生成趋势价格

    data = pd.DataFrame({
        'date': dates,
        'close': prices
    }).set_index('date')

    # 计算布林通道
    bb_data = calculate_bollinger_bands(data, window=20, fill_na=True)

    print(bb_data.head())
    print(bb_data.tail())

    # 可视化
    import matplotlib.pyplot as plt

    plt.figure(figsize=(12,6))
    plt.plot(bb_data['close'], label='Price')
    plt.plot(bb_data['sma'], label='SMA', linestyle='--')
    plt.plot(bb_data['upper_band'], label='Upper Band', color='red')
    plt.plot(bb_data['lower_band'], label='Lower Band', color='green')
    plt.fill_between(bb_data.index,
                    bb_data['lower_band'],
                    bb_data['upper_band'],
                    alpha=0.1,
                    color='orange')
    plt.title('Bollinger Bands')
    plt.legend()
    plt.show()

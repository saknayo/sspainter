import akshare as ak
import pandas as pd
# from sqlalchemy import create_engine
from datetime import datetime

def fecth_daily_data(symbol: str, start_date: str = "20010101", end_date: str = ""):
# def fetch_and_save_daily_data(symbol: str, start_date: str = "20010101"):
    """
    获取股票日频数据并格式化成以下格式
            "日期": "date",
            "开盘": "open",
            "最高": "high",
            "最低": "low",
            "收盘": "close",
            "成交量": "volume"

    :param symbol: 股票代码（如"000002"）
    :param start_date: 数据起始日期（YYYYMMDD格式, 如"20010101"）
    :param end_date: 数据起始日期（YYYYMMDD格式）
    """
    try:
        end_date = datetime.now().strftime("%Y%m%d")
        
        # 获取数据（同原脚本）
        df = ak.stock_zh_a_hist(
            symbol=symbol,
            period="daily",
            start_date=start_date,
            end_date=end_date,
            adjust="hfq"
        )
        
        # 数据清洗（同原脚本）
        df.rename(columns={
            "日期": "date",
            "开盘": "open",
            "最高": "high",
            "最低": "low",
            "收盘": "close",
            "成交量": "volume"
        }, inplace=True)
        df["symbol"] = symbol

        # 创建SQLite引擎[7]
        engine = create_engine(DB_PATH)
        
        # 存储到SQLite（自动创建数据库文件）
        df.to_sql(
            name="daily_price",
            con=engine,
            if_exists="append",
            index=False
        )
        # df.to_csv('stock_data.csv', encoding='gb2312')
        df.to_csv('stock_data.csv', encoding='utf-8')
        print(f"成功保存{symbol} {start_date}-{end_date}数据，记录数：{len(df)}")
        print(df)
        
    except Exception as e:
        print(f"数据获取/存储失败: {str(e)}")

if __name__ == "__main__":
    fetch_and_save_daily_data(symbol="600519")
    '688256'
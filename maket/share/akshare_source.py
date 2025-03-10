import akshare as ak
from datetime import datetime

SHARE_FEATURES = ['date', 'symbol', 'open', 'high', 'low', 'close', 'volume']  # 基础特征+技术指标[8]

class AkShareAdapter:
    def data_format(self, df, symbol):
        if df.empty:
            return
        # 数据清洗
        df.rename(columns={
            "日期": "date",
            "开盘": "open",
            "最高": "high",
            "最低": "low",
            "收盘": "close",
            "成交量": "volume"
        }, inplace=True)
        df["symbol"] = symbol
    
    def fecth_daily_data(self, symbol: str, start_date: str = "20010101", end_date: str = "", adjust = 'hfq'):
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
        :param end_date: 数据起始日期（YYYYMMDD格式）, end_data为空时，默认用当前实时日期
        :param adjust: hfq:后复权 qfq:前复权
        """
        if end_date == '':
            end_date = datetime.now().strftime("%Y%m%d")
        try:
            # 获取数据
            df = ak.stock_zh_a_hist(
                symbol=symbol,
                period="daily",
                start_date=start_date,
                end_date=end_date,
                adjust=adjust # hfq:后复权 qfq:前复权
            )
            # 数据清洗
            self.data_format(df, symbol)
            return df
        except Exception as e:
            print(f"数据获取失败: {str(e)}")

if __name__ == "__main__":
    aj = AkShareAdapter()
    data = aj.fecth_daily_data(symbol="688053")
    print(data)

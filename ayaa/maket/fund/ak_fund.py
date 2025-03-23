import akshare as ak
import pandas as pd
from datetime import datetime

class AkFundAdapter:
    def format_data(self, df, symbol):
        # 重命名列并处理日期格式
        df = df.rename(columns={
            "净值日期": "date",
            "单位净值": "nav",
            "累计净值": "acc_nav"
        })
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        df['symbol'] = symbol
        df['close'] = df['nav']
        df['src'] = 'AK'
        return df
        
    def fetch_daily_data(self, symbol, start_date="20000101", end_date=None):
        """
        从 akshare 获取基金历史净值数据
        自动增量更新：如果数据库已有数据，则只获取最新日期之后的数据
        """
        # 获取数据
        try:
            df = ak.fund_open_fund_info_em(symbol=symbol, indicator="单位净值走势")
            if df.empty:
                print("未获取到数据，请检查基金代码是否正确")
                return None
            
            # 重命名列并处理日期格式
            df = self.format_data(df, symbol)
            # 筛选指定日期范围
            if end_date:
                end_date = pd.to_datetime(end_date).strftime("%Y-%m-%d")
                df = df[df['date'] <= end_date]
            df = df[df['date'] >= pd.to_datetime(start_date).strftime("%Y-%m-%d")]
            
            return df
            
        except Exception as e:
            print(f"数据获取失败: {str(e)}")
            return None

if __name__ == "__main__":
    # 示例：获取易方达蓝筹精选混合（基金代码：005827）
    fund_code = "005827"  # 替换为需要查询的基金代码
    fund_code = '501010'
    start_date = "20230101"  # 初始获取日期
    end_date = datetime.now().strftime("%Y%m%d")  # 截止到今天
                        
    qdapter = AkFundAdapter()
    # 获取并保存数据
    df = qdapter.fetch_daily_data(fund_code, start_date, end_date)
    print(df)

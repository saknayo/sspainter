import pandas as pd
import sqlite3
from datetime import datetime
from ayaa.maket.source_mgr import SourceMgr

# 数据库文件路径
DEFAULT_SHARE_DB_FILE = "share_data.db"
SHARE_FEATURES = ['date', 'symbol', 'open', 'high', 'low', 'close', 'volume', 'src']  # 基础特征+技术指标[8]
FUND_FEATURES = ['date', 'symbol', 'nav', 'src', 'close']  # 基础特征+技术指标[8]

class DataMgr:
    def __init__(self, share_source='AK', fund_source='AK', db_file=''):
        self.adapters = { 
            'share' : SourceMgr.get_share_source_adapter(share_source),
            'fund' : SourceMgr.get_fund_source_adapter(fund_source), }
        self._dbf = DEFAULT_SHARE_DB_FILE if db_file == '' else db_file
        self._dbt = {
            'share' : 'stock_daily',
            'fund' : 'fund_daily',
        }
        self._ft = {
            'share' : SHARE_FEATURES,
            'fund' : FUND_FEATURES,
        }
        self.init_share_db()
        self.init_fund_db()

    def trans_date(self, unstrip_data):
        # 将日期格式从 YYYYMMDD 转换为 YYYY-MM-DD
        return f"{unstrip_data[:4]}-{unstrip_data[4:6]}-{unstrip_data[6:8]}"

    def init_share_db(self):
        """初始化数据库，创建表"""
        with sqlite3.connect(self._dbf) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self._dbt['share']}(
                    symbol TEXT,
                    date TEXT,
                    open REAL,
                    high REAL,
                    low REAL,
                    close REAL,
                    volume REAL,
                    amount REAL,
                    src TEXT,
                    PRIMARY KEY (symbol, date)
                )
            """)
            conn.commit()


    def init_fund_db(self):
        """初始化数据库，创建表"""
        with sqlite3.connect(self._dbf) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self._dbt['fund']} (
                    symbol TEXT,
                    date TEXT,
                    nav REAL,
                    close REAL,
                    src TEXT,
                    PRIMARY KEY (symbol, date)
                )
            """)
            conn.commit()

    def fetch_data_from_db(self, t, symbol, start_date, end_date):
        """从本地数据库获取数据"""
        # 将日期格式从 YYYYMMDD 转换为 YYYY-MM-DD
        start_date = self.trans_date(start_date)
        end_date = self.trans_date(end_date)
        
        # 打印调试信息
        print(f"Querying database for Symbol: {symbol}, Start Date: {start_date}, End Date: {end_date}")
        
        with sqlite3.connect(self._dbf) as conn:
            query = f"""
                SELECT * FROM {self._dbt[t]} 
                WHERE symbol = ? AND date BETWEEN ? AND ?
            """
            df = pd.read_sql_query(query, conn, params=(symbol, start_date, end_date))
        
        # 打印查询结果
        print(f"Query result: {len(df)} records found.")
        return df

    def fetch_all_data_from_db(self, t, symbol):
        """从本地数据库获取数据"""
        with sqlite3.connect(self._dbf) as conn:
            query = f"""
                SELECT * FROM {self._dbt[t]} 
                WHERE symbol = ?  """
            df = pd.read_sql_query(query, conn, params=(symbol,))
        
        # 打印查询结果
        #print(f"Query result: {len(df)} records found.")
        return df

    def save_data_to_db(self, t, symbol, data):
        if data.empty:
            return
        """将数据保存到本地数据库，避免重复插入"""
        with sqlite3.connect(self._dbf) as conn:
            # 检查是否已经存在相同 symbol 和 date 的记录
            existing_dates = pd.read_sql_query(
                f"SELECT date FROM {self._dbt[t]} WHERE symbol = ?", 
                conn, params=(symbol,)
            )["date"].tolist()
            
            # 过滤掉已经存在的数据
            data_to_insert = data[~data["date"].isin(existing_dates)]
            print(data_to_insert)
            data_to_insert = data_to_insert[self._ft[t]] # 筛选出数据库特征数据
        
            # 如果还有新数据，插入到数据库
            if not data_to_insert.empty:
                data_to_insert.to_sql(self._dbt[t], conn, if_exists="append", index=False)
                print(f"Inserted {len(data_to_insert)} new records into the database.")
            else:
                print("No new records to insert.")

    def fetch_all_daily_stock_data(self, t, symbol):
        return self.fetch_all_data_from_db(t, symbol)

    def fetch_daily_stock_data(self, t, symbol, start_date, end_date):
        """
        获取股票每日数据，优先从本地数据库读取
        - 如果数据库中的数据的最新日期等于 end_date，则直接返回数据库中的数据。
        - 如果数据库中的数据的最新日期小于 end_date，则从 akshare 获取缺失的数据。
        """
        # 从数据库查询数据
        db_data = self.fetch_data_from_db(t, symbol, start_date, end_date)
        
        if not db_data.empty:
            # 获取数据库中的最新日期
            latest_date_in_db = db_data["date"].max()
            
            # 如果数据库中的最新日期等于 end_date，直接返回数据库数据
            if latest_date_in_db == self.trans_date(end_date):
                print("Data found in local database and is up to date.")
                return db_data
            
            # 如果数据库中的最新日期小于 end_date，从 akshare 获取缺失的数据
            print(f"Data found in local database, but missing data from {latest_date_in_db} to {end_date}.")
            missing_start_date = (pd.to_datetime(latest_date_in_db) + pd.Timedelta(days=1)).strftime("%Y%m%d")
            missing_data = self.adapters[t].fetch_daily_data(symbol=symbol, start_date=missing_start_date, end_date=end_date)
            
            # 添加股票代码列
            missing_data["symbol"] = symbol
            
            # 保存新数据到数据库
            self.save_data_to_db(t, symbol, missing_data)
            
            # 合并数据库数据和从 akshare 获取的数据
            combined_data = pd.concat([db_data, missing_data], ignore_index=True)
            return combined_data
        
        else:
            # 如果数据库中没有数据，从 akshare 获取全部数据
            print("No data found in local database. Fetching all data from akshare...")
            stock_data = self.adapters[t].fetch_daily_data(symbol=symbol, start_date=start_date, end_date=end_date)
            
            # 添加股票代码列
            stock_data["symbol"] = symbol
            
            # 保存数据到数据库
            self.save_data_to_db(t, symbol, stock_data)
            
            return stock_data

if __name__ == "__main__":
    dm = DataMgr()
    # 示例：获取股票数据
    symbol = "688053"  # 股票代码
    start_date = "20230101"  # 开始日期
    end_date = "20231230"  # 结束日期
    # 获取数据
    data = dm.fetch_daily_stock_data('share', symbol, start_date, end_date)
    # 打印数据
    print(data)

    symbol = "005827"  # 股票代码
    # 获取数据
    data = dm.fetch_daily_stock_data('fund', symbol, start_date, end_date)
    # 打印数据
    print(data)

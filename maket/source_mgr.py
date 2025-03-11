from share.ak_share import AkShareAdapter
from fund.ak_fund import AkFundAdapter

class SourceMgr:
    _share_source_adapter = {
        'AK' : AkShareAdapter,
    }
    _fund_source_adapter = {
        'AK' : AkFundAdapter,
    }

    @classmethod
    def get_share_source_adapter(cls, source_type):
        return cls._share_source_adapter[source_type]()

    @classmethod
    def get_fund_source_adapter(cls, source_type):
        return cls._fund_source_adapter[source_type]()

if __name__ == '__main__':
    adapter = SourceMgr.get_share_source_adapter('AK')
    data = adapter.fetch_daily_data(symbol="688053")
    print(data)
    adapter = SourceMgr.get_fund_source_adapter('AK')
    data = adapter.fetch_daily_data(symbol="005827")
    print(data)

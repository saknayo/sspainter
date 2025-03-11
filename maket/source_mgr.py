from share.akshare_source import AkShareAdapter
from fund.akshare_source import AkFundAdapter

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
    data = adapter.fecth_daily_data(symbol="688053")
    print(data)

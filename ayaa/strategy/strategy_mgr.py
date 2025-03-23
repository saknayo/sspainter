from ayaa.strategy.grid_strategy import GridTradingStrategy
from ayaa.strategy.shan_strategy import ShanTradingStrategy

class StrategyMgr:
    strategies = {
        'Grid' : GridTradingStrategy,
        'Shan' : ShanTradingStrategy,
    }
    @classmethod
    def get_strategy(cls, name):
        return cls.strategies[name] 

if __name__ == '__main__':
    s = StrategyMgr.get_strategy('Grid')(
        grid_num=15,
        lower_bound=25,
        upper_bound=35,
        order_percent=0.08,
        max_position=1000)

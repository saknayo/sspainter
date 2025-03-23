
class TransactionFeeer:
    def __init__(self, buy_fee, sell_fee, mgr_fee): 
        '''
        buy_fee : { amount : fee } 
            amount = price * quantity
            fee : ration charging
        sell_fee : { days : fee }
            days : trade days after buy
            fee : ration charging
        mgr_fee : fee
            fee : every day charging
        '''
        self.buy_fee = buy_fee
        self.sell_fee = sell_fee
        self.mgr_fee = mgr_fee

    def buy_rate(self, amount):
        # amount = price * quantity
        for k in reversed(list(self.buy_fee.keys())):
            if k < amount:
                return self.buy_fee[k]

    def sell_rate(self, days):
        for k in reversed(list(self.sell_fee.keys())):
            if k <= days:
                return self.sell_fee[k]
        
if __name__ == '__main__':
    buy_fee = { 0 : 0.0015, 10000 : 0.001 }
    sell_fee = { 0 : 0.015, 7 : 0.0075, 30 : 0}
    mgr_fee = 0
    config = (buy_fee, sell_fee, mgr_fee)
    fmgr = TransactionFeeer(*config)
    print('expect:0.0015 calc:', fmgr.buy_rate(9999))
    print('expect:0.0015 calc:', fmgr.buy_rate(10000))
    print('expect:0.001 calc:', fmgr.buy_rate(10001))
    print('expect:0.001 calc:', fmgr.buy_rate(1000000))
    print('expect:0.015 calc:', fmgr.sell_rate(1))
    print('expect:0.015 calc:', fmgr.sell_rate(7))
    print('expect:0.0075 calc:', fmgr.sell_rate(8))
    print('expect:0.0075 calc:', fmgr.sell_rate(29))
    print('expect:0.0075 calc:', fmgr.sell_rate(30))
    print('expect:0 calc:', fmgr.sell_rate(31))


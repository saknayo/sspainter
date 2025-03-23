from ayaa.utils.fee_mgr import TransactionFeeer
from ayaa.utils.trade_day import calc_hold_days

class FinanceMgr:
    def __init__(self, init_cash, buy_max_fee, sell_max_fee, fee_config): 
        self.init_cash = init_cash
        self.current_cash = self.init_cash
        self.total_holding = 0
        self.holdings = []
        self.buy_max_fee = buy_max_fee
        self.sell_max_fee = sell_max_fee
        self.feeer = TransactionFeeer(*fee_config)

    def get_total_value(self, current_price):
        return self.current_cash + self.total_holding * current_price

    def get_profit(self, current_price):
        total_value = self.current_cash + self.total_holding * current_price
        return (total_value - self.init_cash) / self.init_cash

    def get_holding_ration(self, current_price):
        return self.total_holding * current_price / self.get_total_value(current_price)

    def reset(self):
        self.init_cash = 0
        self.current_cash = self.init_cash
        self.total_holding = 0
        self.holdings = []
        self.buy_max_fee = 0
        self.sell_max_fee = 0
 
    def buy(self, current_date, current_price, quantity):
        # buy_fee = self.get_fee('buy', current_date, quantity=)
        need_cash = current_price * quantity
        avaliable_cash = min(need_cash, self.current_cash)
        trade_quantity = avaliable_cash / current_price
        self.current_cash -= avaliable_cash
        self.total_holding += trade_quantity
        self.holdings.append({
            'date': current_date,
            'price': current_price,
            'quantity' : trade_quantity,
        })
        return trade_quantity

    def sell(self, current_date, current_price, quantity):
        need_quantity = quantity
        sell_trades = []
        for h in self.holdings:
            sell_fee = self.get_sell_fee(sell_date=current_date, buy_date=h['date'])
            # print('sell_fee:', sell_fee)
            if sell_fee <= self.sell_max_fee:
                sell_quantity = min(need_quantity, h['quantity'])
                need_quantity -= sell_quantity
                h['quantity'] -= sell_quantity
                sell_trades.append({'price' : current_price, 'quantity' : sell_quantity, 'fee' : sell_fee})
                if need_quantity == 0:
                    break

        avaliable_quantity = quantity - need_quantity
        self.total_holding -= avaliable_quantity
        sell_cash = sum(t['quantity'] * (1 - t['fee']) for t in sell_trades) * current_price
        self.current_cash += sell_cash
        return avaliable_quantity


    def get_buy_fee(self, current_price, quantity):
        amount = current_price * quantity
        return self.feeer.buy_rate(amount)

    def get_sell_fee(self, sell_date, buy_date):
        hold_days = calc_hold_days(buy_date, sell_date)
        # print('hold_days:', hold_days)
        return self.feeer.sell_rate(hold_days)
        
if __name__ == '__main__':
    buy_fee = { 0 : 0.0015, 10000 : 0.001 }
    sell_fee = { 0 : 0.015, 7 : 0.0075, 30 : 0}
    mgr_fee = 0
    fee_config = (buy_fee, sell_fee, mgr_fee)
    fm = FinanceMgr(init_cash=100000, buy_max_fee=0.001, sell_max_fee=0.0075, fee_config=fee_config)
    bty = fm.buy('2024-03-21', 30, 300)
    print('Buy:', bty)
    sty = fm.sell('2024-03-22', 30, 310)
    print('Sell:', sty)
    sty = fm.sell('2024-03-28', 30, 310)
    print('Sell:', sty)
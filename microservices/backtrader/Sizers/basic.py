# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Datetime : 2020/10/16 20:17
# @Author   : Fangyang
# @Software : PyCharm


import backtrader as bt
from datetime import datetime
import math


class exampleSizer(bt.Sizer):
    params = (('size', 1),)

    def _getsizing(self, comminfo, cash, data, isbuy):
        return self.p.size


class printSizingParams(bt.Sizer):
    '''
    Prints the sizing parameters and values returned from class methods.
    '''

    def _getsizing(self, comminfo, cash, data, isbuy):
        # Strategy Method example
        pos = self.strategy.getposition(data)
        # Broker Methods example
        acc_value = self.broker.getvalue()

        # Print results
        print('----------- SIZING INFO START -----------')
        print('--- Strategy method example')
        print(pos)
        print('--- Broker method example')
        print('Account Value: {}'.format(acc_value))
        print('--- Param Values')
        print('Cash: {}'.format(cash))
        print('isbuy??: {}'.format(isbuy))
        print('data[0]: {}'.format(data[0]))
        print('------------ SIZING INFO END------------')

        return 0


class maxRiskSizer(bt.Sizer):
    '''
    Returns the number of shares rounded down that can be purchased for the
    max rish tolerance
    '''
    params = (('risk', 0.03),)

    def __init__(self):
        if self.p.risk > 1 or self.p.risk < 0:
            raise ValueError('The risk parameter is a percentage which must be'
                             'entered as a float. e.g. 0.5')

    def _getsizing(self, comminfo, cash, data, isbuy):
        if isbuy == True:
            size = math.floor((cash * self.p.risk) / data[0])
        else:
            size = math.floor((cash * self.p.risk) / data[0]) * (-1)
        return size


class maxRiskSizerComms(bt.Sizer):
    '''
    Returns the number of shares rounded down that can be purchased for the
    max risk tolerance
    '''
    params = (('risk', 0.1),
              ('debug', True))

    def _getsizing(self, comminfo, cash, data, isbuy):
        size = 0

        # Work out the maximum size assuming all cash can be used.
        max_risk = math.floor(cash * self.p.risk)

        comm = comminfo.p.commission

        if comminfo.stocklike:  # We are using a percentage based commissions

            # Apply the commission to the price. We can then divide our risk
            # by this value
            com_adj_price = data[0] * (1 + (comm * 2))  # *2 for round trip
            comm_adj_max_risk = "N/A"

            if isbuy == True:
                comm_adj_size = max_risk / com_adj_price
                if comm_adj_size < 0:  # Avoid accidentally going short
                    comm_adj_size = 0
            else:
                comm_adj_size = max_risk / com_adj_price * -1

        else:  # Else is fixed size
            # Dedecut commission from available cash to invest
            comm_adj_max_risk = max_risk - (comm * 2)  # Round trip
            com_adj_price = "N/A"

            if comm_adj_max_risk < 0:  # Not enough cash
                return 0

            if isbuy == True:
                comm_adj_size = comm_adj_max_risk / data[0]
            else:
                comm_adj_size = comm_adj_max_risk / data[0] * -1

        # Finally make sure we round down to the nearest unit.
        comm_adj_size = math.floor(comm_adj_size)

        if self.p.debug:
            if isbuy:
                buysell = 'Buying'
            else:
                buysell = 'Selling'
            print("------------- Sizer Debug --------------")
            print("Action: {}".format(buysell))
            print("Price: {}".format(data[0]))
            print("Cash: {}".format(cash))
            print("Max Risk %: {}".format(self.p.risk))
            print("Max Risk $: {}".format(max_risk))
            print("Commission Adjusted Max Risk: {}".format(comm_adj_max_risk))
            print("Current Price: {}".format(data[0]))
            print("Commission: {}".format(comm))
            print("Commission Adj Price (Round Trip): {}".format(com_adj_price))
            print("Size: {}".format(comm_adj_size))
            print("----------------------------------------")
        return comm_adj_size


class firstStrategy(bt.Strategy):

    def __init__(self):
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=21)

    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.buy()
        else:
            if self.rsi > 70:
                self.close()

    def notify_trade(self, trade):
        if trade.justopened:
            print('----TRADE OPENED----')
            print('Size: {}'.format(trade.size))
        elif trade.isclosed:
            print('----TRADE CLOSED----')
            print('Profit, Gross {}, Net {}'.format(
                round(trade.pnl, 2),
                round(trade.pnlcomm, 2)))
        else:
            return


if __name__ == '__main__':
    # Variable for our starting cash
    startcash = 10000

    # Create an instance of cerebro
    cerebro = bt.Cerebro()

    # Add our strategy
    cerebro.addstrategy(firstStrategy)

    # Get Apple data from Yahoo Finance.
    data = bt.feeds.YahooFinanceData(
        dataname='AAPL',
        fromdate=datetime(2016, 1, 1),
        todate=datetime(2017, 1, 1),
        buffered=True
    )

    # Add the data to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(startcash)

    # add the sizer
    cerebro.addsizer(printSizingParams)

    # Run over everything
    cerebro.run()

    # Get final portfolio Value
    portvalue = cerebro.broker.getvalue()
    pnl = portvalue - startcash

    # Print out the final result
    print('----SUMMARY----')
    print('Final Portfolio Value: ${}'.format(portvalue))
    print('P/L: ${}'.format(pnl))

    # Finally plot the end results
    cerebro.plot(style='candlestick')

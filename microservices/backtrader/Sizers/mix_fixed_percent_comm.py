# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Datetime : 2020/10/16 22:01
# @Author   : Fangyang
# @Software : PyCharm

import backtrader as bt


class stampDutyCommissionScheme(bt.CommInfoBase):
    '''
    This commission scheme uses a fixed commission and stamp duty for share
    purchases. Share sales are subject only to the fixed commission.

    The scheme is intended for trading UK equities on the main market.
    '''
    params = (
        ('stamp_duty', 0.005),
        ('commission', 5),
        ('stocklike', True),
        ('commtype', bt.CommInfoBase.COMM_FIXED),
    )

    def _getcommission(self, size, price, pseudoexec):
        '''
        If size is greater than 0, this indicates a long / buying of shares.
        If size is less than 0, it idicates a short / selling of shares.
        '''

        if size > 0:
            return self.p.commission + (size * price * self.p.stamp_duty)
        elif size < 0:
            return self.p.commission
        else:
            return 0  # just in case for some reason the size is 0.


if __name__ == '__main__':
    # Create an instance of cerebro
    cerebro = bt.Cerebro()

    # Add the new commissions scheme
    comminfo = stampDutyCommissionScheme()
    cerebro.broker.addcommissioninfo(comminfo)

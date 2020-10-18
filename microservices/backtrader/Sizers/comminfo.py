# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Datetime : 2020/10/16 21:52
# @Author   : Fangyang
# @Software : PyCharm

import backtrader as bt


class FixedCommisionScheme(bt.CommInfoBase):
    '''
    This is a simple fixed commission scheme
    '''
    params = (
        ('commission', 5),
        ('stocklike', True),
        ('commtype', bt.CommInfoBase.COMM_FIXED),
    )

    def _getcommission(self, size, price, pseudoexec):
        return self.p.commission


if __name__ == '__main__':

    cerebro = bt.Cerebro()
    # If the margin variable is set,
    # it assumes you are trading a futures contract
    # and sets the commission to be fixed

    # cerebro.broker.setcommission(commission=10, margin=2000, mult=10)

    # comminfo instance.
    # This allows you to access commission attributes (variables)
    # such as commission, mult and marginas well as comminfo’s own methods (functions)

    # Set commissions
    comminfo = FixedCommisionScheme()
    cerebro.broker.addcommissioninfo(comminfo)
    pass

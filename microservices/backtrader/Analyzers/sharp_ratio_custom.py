# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Datetime : 2020/10/11 15:32
# @Author   : Fangyang
# @Software : PyCharm


from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import operator

from backtrader.utils.py3 import map
from backtrader import Analyzer, TimeFrame
from backtrader.mathsupport import average, standarddev
from backtrader.analyzers import AnnualReturn


class SharpeRatio(Analyzer):
    params = (
        ('timeframe', TimeFrame.Years),
        ('riskfreerate', 0.01),
    )

    def __init__(self):
        super(SharpeRatio, self).__init__()
        self.anret = AnnualReturn()

    def start(self):
        # Not needed ... but could be used
        pass

    def next(self):
        # Not needed ... but could be used
        pass

    def stop(self):
        retfree = [self.p.riskfreerate] * len(self.anret.rets)
        retavg = average(list(map(operator.sub, self.anret.rets, retfree)))
        retdev = standarddev(self.anret.rets)

        self.ratio = retavg / retdev

    def get_analysis(self):
        return dict(sharperatio=self.ratio)


if __name__ == '__main__':
    pass

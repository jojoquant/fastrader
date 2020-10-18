# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Datetime : 2020/10/8 14:20
# @Author   : Fangyang
# @Software : PyCharm

from microservices.utils.format import trans_vnpy_to_backtrader_df_col_name_OHLCI
from microservices.backtrader.DataFeeds.trader.setting import get_settings
from microservices.backtrader.DataFeeds.db_operation import DBOperation


def gen_backtrader_data_df(dbbardata_info_dict, dbo):
    # data = dbo.get_bar_data(**dbbardata_info_dict)
    # df = dbo.get_bar_data_df(**dbbardata_info_dict)
    return trans_vnpy_to_backtrader_df_col_name_OHLCI(dbo.get_bar_data_df(**dbbardata_info_dict))


if __name__ == '__main__':
    pass

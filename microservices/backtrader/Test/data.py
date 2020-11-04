# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Datetime : 2020/10/11 13:15
# @Author   : Fangyang
# @Software : PyCharm

from microservices.utils.format import trans_vnpy_to_backtrader_df_col_name_OHLCI
from microservices.database.sqlite.trader.setting import get_settings
from microservices.database.sqlite.pandas_operation import DBOperation


def gen_test_data_df(dbbardata_info_dict=None, dbo=None):
    if not dbo:
        settings = get_settings("database.")
        dbo = DBOperation(settings_dict=settings)

    if not dbbardata_info_dict:
        dbbardata_info_dict = {
            "symbol": "AL8",
            "exchange": "DCE",
            "interval": "1h",
            "start": "2015-01-01 23:58:02",
            "end": "2020-02-01 23:58:02"
        }

    return trans_vnpy_to_backtrader_df_col_name_OHLCI(dbo.get_bar_data_df(**dbbardata_info_dict))


if __name__ == '__main__':
    df = gen_test_data_df()
    print(1)

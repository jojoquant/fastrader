# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Datetime : 2020/10/8 15:11
# @Author   : Fangyang
# @Software : PyCharm


from pandas import DataFrame


def trans_vnpy_to_backtrader_df_col_name_OHLCI(df: DataFrame) -> DataFrame:
    df.rename(
        columns={
            'open_price': 'open',
            'high_price': 'high',
            'low_price': 'low',
            'close_price': 'close',
            'open_interest': 'openinterest'
        },
        inplace=True)
    return df


def trans_backtrader_to_vnpy_df_col_name_OHLCI(df: DataFrame) -> DataFrame:
    return df.rename(
        columns={
            'open': 'open_price',
            'high': 'high_price',
            'low': 'low_price',
            'close': 'close_price',
            'openinterest': 'open_interest'
        },
        inplace=True)


if __name__ == '__main__':
    pass

#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Datetime :   2020/1/24 下午8:23
@Author   :   Fangyang
"""
import sys

# import os
# print(os.path.abspath('..'))
sys.path.append('..')  # 临时添加microservices到环境变量中

from functools import lru_cache
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import platform

from microservices.backtrader.DataFeeds.trader.utility import get_file_path
from microservices.utils.timeit import timeit_cls_method_wrapper


class DBOperation:
    def __init__(self, settings_dict):
        self.settings_dict = settings_dict
        self.file_path_str = get_file_path(settings_dict['database'])

        os_str = platform.system()
        if os_str == "Windows":
            sqlite_os = "/"
        elif os_str == "Linux":
            sqlite_os = "//"
        else:
            print(f"OS is {os_str}. DBoperation may meet problem.")

        self.engine = create_engine(f"{self.settings_dict['driver']}://{sqlite_os}{self.file_path_str}")

    def get_groupby_data_from_sql_db(self):
        sql = "select exchange, symbol, interval, count(1) from dbbardata group by symbol, interval, exchange;"
        return pd.read_sql(sql, con=self.engine)

    def get_end_date_from_db(self, symbol, exchange, interval):
        sql = f'''select * from dbbardata 
        where symbol='{symbol}' and exchange='{exchange}' and interval='{interval}' 
        order by datetime desc limit 1;
        '''
        df = pd.read_sql(sql, con=self.engine)
        return df['datetime'].values[0]

    def get_start_date_from_db(self, symbol, exchange, interval):
        sql = f'''select * from dbbardata 
        where symbol='{symbol}' and exchange='{exchange}' and interval='{interval}' 
        order by datetime asc limit 1;
        '''
        df = pd.read_sql(sql, con=self.engine)
        # str '2013-08-19 15:00:00'
        return df['datetime'].values[0]

    @lru_cache(maxsize=999)
    @timeit_cls_method_wrapper
    def get_bar_data_df(self, symbol, exchange, interval, start=None, end=None):
        datetime_start = f" and datetime >= '{start}'" if start else ""
        datetime_end = f" and datetime <= '{end}'" if end else f" and datetime <= '{datetime.now()}'"

        sql = f'''select * from dbbardata 
        where symbol='{symbol}' and exchange='{exchange}' and interval='{interval}'
        {datetime_start} {datetime_end}; 
        '''
        df = pd.read_sql(sql, con=self.engine).drop('id', axis=1)
        df['datetime'] = pd.to_datetime(df['datetime'])
        return df


if __name__ == "__main__":
    from microservices.backtrader.DataFeeds.trader.setting import get_settings

    settings = get_settings("database.")
    dbo = DBOperation(settings)
    # dbo.get_start_date_from_db()
    # xx = dbo.get_groupby_data_from_sql_db()

    dbbardata_info_dict = {
        "symbol": "RBL8",
        "exchange": "SHFE",
        "interval": "1m",
        "end": "2015-11-26 23:58:02"
    }

    # data = dbo.get_bar_data(**dbbardata_info_dict)
    df = dbo.get_bar_data_df(**dbbardata_info_dict)

    # for row in df.iterrows():
    #     print(1)
    # print(1)

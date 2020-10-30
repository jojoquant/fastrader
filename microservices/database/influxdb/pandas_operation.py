# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Datetime : 2020/10/25 17:15
# @Author   : Fangyang
# @Software : PyCharm

from influxdb import DataFrameClient
import pandas as pd


class InfluxDB(object):
    def __init__(
            self, host: str = 'localhost', port: int = 8086,
            username: str = "user", password: str = "Cisc0123",
            database: str = "DBfastrader"):
        self.client = DataFrameClient(host=host, port=port, username=username, password=password, database=database)

    def write_df_to_db(self, df: pd.DataFrame,
                       protocol: str = 'line', measurement: str = "financial",
                       batch_size: int = 1000):
        self.client.write_points(df, measurement, tag_columns=['code'], protocol=protocol, batch_size=batch_size)


if __name__ == '__main__':
    pass

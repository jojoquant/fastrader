# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Datetime : 2020/10/20 23:04
# @Author   : Fangyang
# @Software : PyCharm

import pandas as pd

from influxdb import InfluxDBClient
from influxdb import DataFrameClient


def basic_using():
    client = InfluxDBClient(host='localhost', port='8086', username='admin', password="Cisc0123")

    # 查看数据库
    print(client.get_list_database())

    # 创建数据库
    print(client.create_database('testdb'))
    print(client.get_list_database())

    # 删除数据库
    print(client.drop_database('testdb'))
    print(client.get_list_database())

    # 用user账户连接
    client = InfluxDBClient(host='localhost', port='8086', username='user1', password="Cisc0123",
                            database='DBfastrader')
    # 显示数据库中的表
    r = client.query('show measurements;')
    print(r)


def pandas_using(df:pd.DataFrame=None):
    protocol = 'line'
    dbname = 'DBfastrader'
    client = DataFrameClient(host='localhost', port='8086', username='user1', password="Cisc0123", database=dbname)
    if df is None:
        df = pd.DataFrame(data=list(range(30)),
                          index=pd.date_range(start='2014-11-16',
                                              periods=30, freq='H'), columns=['0'])

    print("Delete database: " + dbname)
    client.drop_database(dbname)

    print("Create database: " + dbname)
    client.create_database(dbname)

    print("Write DataFrame")
    client.write_points(df, 'demo', tag_columns=['code'], protocol=protocol)

    # print("Write DataFrame with Tags")
    # client.write_points(df, 'demo',
    #                     {'k1': 'v1', 'k2': 'v2'}, protocol=protocol)

    print("Read DataFrame")
    r = client.query("select * from demo")
    print(r)

    # print("Delete database: " + dbname)
    # client.drop_database(dbname)


if __name__ == '__main__':
    df = pd.read_csv('fin_test.csv')
    df['report_date'] = pd.to_datetime(df['report_date'], format="%Y%m%d")
    df = df.set_index('report_date')
    pandas_using(df)

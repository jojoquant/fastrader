# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Datetime : 2020/10/20 23:04
# @Author   : Fangyang
# @Software : PyCharm

import pandas as pd
import time
from influxdb import InfluxDBClient
from influxdb import DataFrameClient

import matplotlib.pyplot as plt


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

    r = client.query("select EPS from demo where code='703';")
    print(r)


def pandas_using(df: pd.DataFrame = None):
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

    start_time = time.perf_counter()
    print("Write DataFrame")
    client.write_points(df, 'demo', tag_columns=['code'], protocol=protocol, batch_size=1000)
    print(f'Write {len(df)} csv data cost: {time.perf_counter() - start_time:.2f}s')
    # print("Write DataFrame with Tags")
    # client.write_points(df, 'demo',
    #                     {'k1': 'v1', 'k2': 'v2'}, protocol=protocol)

    # print("Read DataFrame")
    # r = client.query("select * from demo")
    # print(r)

    # print("Delete database: " + dbname)
    # client.drop_database(dbname)


def pandas_influxdb_condition_query(
        start='2020-07-31',
        end='now()',
        code=None,
        columns=['code', 'ROE', 'netAssetsPerShare'],
        conditions=["ROE>-10", "ROE<10"]
):
    protocol = 'line'
    dbname = 'DBfastrader'
    client = DataFrameClient(host='localhost', port='8086', username='user1', password="Cisc0123", database=dbname)

    measure = "demo"

    print("Read DataFrame")
    start_time = time.perf_counter()
    columns_str = ",".join(columns)
    conditions_str = " and ".join(conditions)
    sql_str = f"select {columns_str} from {measure} where time>'{start}' and time<{end} and {conditions_str};"
    r = client.query(sql_str)
    print(f"Query time cost: {time.perf_counter() - start_time:.2f}s")
    df = pd.DataFrame(r[measure])
    plt.hist(df["ROE"], bins=100)
    plt.show()
    print(r)


def pandas_influxdb_show_code(
        measure="demo",
        start='2020-07-31',
        end='now()',
        code=None,
        columns=['code'],
):
    protocol = 'line'
    dbname = 'DBfastrader'
    # client = DataFrameClient(host='localhost', port='8086', username='user1', password="Cisc0123", database=dbname)
    client = InfluxDBClient(host='localhost', port='8086', username='admin', password="Cisc0123", database=dbname)

    print("Read DataFrame")
    start_time = time.perf_counter()
    columns_str = ",".join(columns)

    series_str = "series"
    func_str = "mean"
    func_value = "EPS"
    group_by_str = "code"
    time_str = 'time'
    sql_str = f'select {func_str}("{func_value}") from demo where {time_str}>\'2019-12-30\' group by {group_by_str};'
    print(sql_str)
    r = client.query(sql_str)
    print(f"Query time cost: {time.perf_counter() - start_time:.2f}s")
    # r_list = [pd.DataFrame.from_dict(s[0]) for s in r]
    r_dict = {time_str: [], func_str: []}
    for idx, r_list in enumerate(r):
        print(idx)
        r_dict[time_str].append(r_list[0][time_str])
        r_dict[func_str].append(r_list[0][func_str])

    print(1)

    r_df = pd.DataFrame()
    for idx, s in enumerate(r):
        s_dict = s[0]
        df = pd.DataFrame.from_dict(s_dict, orient='index').T
        r_df = r_df.append(df)
        print(idx)

    # df = pd.concat(r_list, ignore_index=True)
    # df = pd.DataFrame(r)
    print(1)


def _ix2df(series):
    df = pd.DataFrame.from_dict(series[0])
    return df


if __name__ == '__main__':
    # start_time = time.perf_counter()
    # df = pd.read_csv('../datasource/pytdx/financial/financial_data.csv')
    # print(f'Load csv data cost: {time.perf_counter()-start_time:.2f}s')
    # df['report_date'] = pd.to_datetime(df['report_date'], format="%Y%m%d")
    # df = df.set_index('report_date')
    # pandas_using(df)

    # basic_using()

    # pandas_influxdb_condition_query()
    pandas_influxdb_show_code()

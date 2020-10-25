# !/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
created by Fangyang on Time:2018/10/28
'''
__author__ = 'Fangyang'

import pandas as pd
import json
import time

from typing import Tuple
from tqdm import tqdm
from pymongo import MongoClient


class MongoDB(object):

    def __init__(self, host: str = 'localhost', port: int = 27017,
                 username: str = None, password: str = None):
        self.client = MongoClient(host=host, port=port, username=username, password=password)

    def read_db(self,
                database_name: str = 'DBfastrader',
                collection_name: str = 'financial',
                query: Tuple[dict, dict] = (dict(), {'_id': 0})):

        db = self.client[database_name]
        collection = db[collection_name]
        start_time = time.perf_counter()
        df = pd.DataFrame(list(collection.find(*query)))
        print('Read data from mongo cost:{:.2f}s'.format(time.perf_counter() - start_time))
        return df

    def write_df_dict_to_db(self,
                            df: pd.DataFrame,
                            database_name: str = 'mydatabasename',
                            collection_name: str = 'mycollectionname',
                            delete_old_collection: bool = True,
                            chunksize: int = None,
                            timer: bool = True):
        """
        将 dataframe 转成 list[dict] 后写入 mongodb, 如果df的col有重名, 在转dict过程中会丢失列
        :param df:
        :param database_name:
        :param collection_name:
        :param delete_old_collection:
        :param chunksize:
        :param timer:
        :return:
        """

        # To connect
        db = self.client[database_name]
        collection = db[collection_name]
        # To write
        if delete_old_collection:
            collection.delete_many({})  # Destroy the collection
        # aux_df=aux_df.drop_duplicates(subset=None, keep='last') # To avoid repetitions

        if timer:
            start_time = time.perf_counter()

        my_list = df.to_dict('records')

        nrows = len(my_list)
        if nrows == 0:
            return

        if chunksize is None:
            chunksize = nrows
        elif chunksize == 0:
            raise ValueError('chunksize argument should be non-zero')

        chunks = int(nrows / chunksize) + 1
        pbar = tqdm(range(chunks), initial=1)

        for i in pbar:
            start_i = i * chunksize
            end_i = min((i + 1) * chunksize, nrows)
            if start_i >= end_i:
                break
            pbar.set_description(f"Start write data into mongodb->{database_name}->{collection_name}")
            collection.insert_many(my_list[start_i:end_i])

        if timer:
            pbar.set_description('Complete importing data to DB:{} -- collection:{}. Time cost : {:.2f}s'.format(
                database_name, collection_name, time.perf_counter() - start_time))
        else:
            pbar.set_description('Complete importing data to DB:{} -- collection:{}.'.format(
                database_name, collection_name))
        return


def write_df_json_to_db(self,
                        my_df: pd.DataFrame,
                        database_name: str = 'mydatabasename',
                        collection_name: str = 'mycollectionname',
                        delete_old_collection: bool = True,
                        timer: bool = True):
    '''
    三种写入数据的方式中最快, 快10多秒钟, 其他两种方式有chunksize的效果一般
    缺点是 df.to_json(orient='records', date_format="iso") 以后,
    再json.loads 生成dict里面的date会变成字符串, 需要加钩子函数去遍历列转成标准python的datetime格式, 影响效率
    :param my_df: Dataframe
    :param database_name: str
    :param collection_name: str
    :param delete_old_collection: Boolean
    :param timer: Boolean
    :return: None
    '''

    db = self.client[database_name]
    collection = db[collection_name]

    if delete_old_collection:
        collection.delete_many({})  # Destroy the collection

    if timer:
        start_time = time.perf_counter()

    collection.insert_many(json.loads(my_df.to_json(orient='records')))

    if timer:
        print('Complete importing data to DB:{} -- collection:{}. Time cost : {:.2f}s'.format(
            database_name, collection_name, time.perf_counter() - start_time))
    else:
        print('Complete importing data to DB:{} -- collection:{}.'.format(
            database_name, collection_name))
    return


if __name__ == '__main__':
    pd_mongo = MongoDB()
    start_time = time.perf_counter()
    # df = pd.read_csv('../../datasource/pytdx/financial/financial_data.csv')
    df = pd.read_csv('../influxdb/fin_test.csv')
    df['report_date'] = pd.to_datetime(df['report_date'], format='%Y%m%d', utc=False)
    df['report_date'] = df['report_date'].dt.tz_localize('Asia/Shanghai')  # 设置当前时间为东八区
    df['report_date'] = df['report_date'].dt.tz_convert('UTC')  # 转成utc时间
    # df.set_index("report_date", inplace=True)
    df.columns = [i.replace('.', '_') for i in df.columns]
    # 生成_id
    df["_id"] = df["report_date"].apply(lambda x: x.strftime("%Y%m%d")) \
                + df['code'].apply(lambda x: '{:0>6d}'.format(x))
    print(f"Read csv data cost: {time.perf_counter() - start_time:.2f}s")

    # pd_mongo.write_df_dict_to_db(df, collection_name='from_df_list_nochunk')
    # pd_mongo.write_df_dict_to_db(df, collection_name='from_df_list_chunksize100', chunksize=5000)
    write_start_time = time.perf_counter()
    pd_mongo.write_df_dict_to_db(df, database_name="DBfastrader", collection_name='financial', chunksize=1000)
    print(f"Write csv data cost: {time.perf_counter() - write_start_time:.2f}s")

    # dff = pd_mongo.read_db(database_name="DBfastrader", collection_name='financial')
    # dff['report_date'] = dff['report_date'].dt.tz_localize('UTC')
    # dff['report_date'] = dff['report_date'].dt.tz_convert('Asia/Shanghai')
    # print(1)

    # Complete importing data to DB:mydatabasename -- collection:from_df_list_nochunk. Time cost : 46.07s
    # Complete importing data to DB:mydatabasename -- collection:from_df_list_chunksize100. Time cost : 45.45s
    # Complete importing data to DB:mydatabasename -- collection:from_df_json. Time cost : 35.21s

    # 'Read data from mongo cost : 12.95s'
    # 'Read data from mysql cost : 39.89s'

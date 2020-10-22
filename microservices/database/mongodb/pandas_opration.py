# !/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
created by Fangyang on Time:2018/10/28
'''
__author__ = 'Fangyang'

import pandas as pd
from pymongo import MongoClient
import json
import time


class MongoDB(object):

    def __init__(self, host: str = 'localhost', port: int = 27017, username=None, password=None):
        self.client = MongoClient(host=host, port=port, username=username, password=password)

    def read_db(self,
                database_name='mydatabasename',
                collection_name='mycollectionname',
                query=(dict(), {'_id': 0})):

        db = self.client[database_name]
        collection = db[collection_name]
        start_time = time.time()
        df = pd.DataFrame(list(collection.find(*query)))
        print('read data from mongo cost:{:.2f}s'.format(time.time() - start_time))
        return df

    def write_df_list_to_db(self,
                            my_df,
                            database_name='mydatabasename',
                            collection_name='mycollectionname',
                            chunksize=None,
                            timer=True):
        # """
        # This function take a list and create a collection in MongoDB (you should
        # provide the database name, collection, port to connect to the remoete database,
        # server of the remote database, local port to tunnel to the other machine)
        #
        # ---------------------------------------------------------------------------
        # Parameters / Input
        #    my_list: the list to send to MongoDB
        #    database_name:  database name
        #
        #    collection_name: collection name (to create)
        #    server: the server of where the MongoDB database is hosted
        #        Example: server = '132.434.63.86'
        #    this_machine_port: local machine port.
        #        For example: this_machine_port = '27017'
        #    remote_port: the port where the database is operating
        #        For example: remote_port = '27017'
        #    chunksize: The number of items of the list that will be send at the
        #        some time to the database. Default is None.
        # ----------------------------------------------------------------------------

        # To connect
        db = self.client[database_name]
        collection = db[collection_name]
        # To write
        collection.delete_many({})  # Destroy the collection
        # aux_df=aux_df.drop_duplicates(subset=None, keep='last') # To avoid repetitions

        if timer:
            start_time = time.time()

        my_list = my_df.to_dict('records')
        nrows = len(my_list)
        if nrows == 0:
            return

        if chunksize is None:
            chunksize = nrows
        elif chunksize == 0:
            raise ValueError('chunksize argument should be non-zero')

        chunks = int(nrows / chunksize) + 1

        for i in range(chunks):
            start_i = i * chunksize
            end_i = min((i + 1) * chunksize, nrows)
            if start_i >= end_i:
                break
            collection.insert_many(my_list[start_i:end_i])

        if timer:
            print('Complete importing data to DB:{} -- collection:{}. Time cost : {:.2f}s'.format(
                database_name, collection_name, time.time() - start_time))
        else:
            print('Complete importing data to DB:{} -- collection:{}.'.format(
                database_name, collection_name))
        return

    def write_df_json_to_db(self,
                            my_df,
                            database_name='mydatabasename',
                            collection_name='mycollectionname',
                            timer=True):
        '''
        三种写入数据的方式中最快, 快10多秒钟, 其他两种方式有chunksize的效果一般
        :param my_df: Dataframe
        :param database_name: str
        :param collection_name: str
        :param server: str
        :param mongodb_port: int/str
        :param timer: Boolean
        :return: None
        '''

        db = self.client[database_name]
        collection = db[collection_name]
        collection.delete_many({})  # Destroy the collection

        if timer:
            start_time = time.time()

        collection.insert_many(json.loads(my_df.to_json(orient='records')))

        if timer:
            print('Complete importing data to DB:{} -- collection:{}. Time cost : {:.2f}s'.format(
                database_name, collection_name, time.time() - start_time))
        else:
            print('Complete importing data to DB:{} -- collection:{}.'.format(
                database_name, collection_name))
        return


if __name__ == '__main__':
    pd_mongo = MongoDB()
    start_time = time.perf_counter()
    df = pd.read_csv('../../datasource/pytdx/financial/financial_data.csv')
    df.columns = [i.replace('.', '_') for i in df.columns]
    print(f"Read csv data cost: {time.perf_counter()-start_time:.2f}s")

    # pd_mongo.write_df_list_to_db(df, collection_name='from_df_list_nochunk')
    # pd_mongo.write_df_list_to_db(df, collection_name='from_df_list_chunksize100', chunksize=5000)
    write_start_time = time.perf_counter()
    pd_mongo.write_df_json_to_db(df, database_name="DBfastrader", collection_name='financial')
    print(f"Write csv data cost: {time.perf_counter() - write_start_time:.2f}s")

    # Complete importing data to DB:mydatabasename -- collection:from_df_list_nochunk. Time cost : 46.07s
    # Complete importing data to DB:mydatabasename -- collection:from_df_list_chunksize100. Time cost : 45.45s
    # Complete importing data to DB:mydatabasename -- collection:from_df_json. Time cost : 35.21s

    # 'Read data from mongo cost : 12.95s'
    # 'Read data from mysql cost : 39.89s'

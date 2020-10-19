# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Datetime : 2020/10/19 17:03
# @Author   : Fangyang
# @Software : PyCharm

import time
from typing import List
import pandas as pd
from tqdm import tqdm

from pytdx.crawler.history_financial_crawler import HistoryFinancialListCrawler, HistoryFinancialCrawler
from microservices.datasource.pytdx.financial.financial_mean import financial_dict

# from pytdx.crawler.base_crawler import demo_reporthook


def download_financial_data(report_date: List[str] = None) -> pd.DataFrame:
    '''
    下载金融财务数据
    :param report_date: default None, 表示下载全部数据. 指定下载格式为 ["20200930", "20200630", "20200331", "20191231"], 其他格式和月日数字不行
    :return: 财务数据拼接的 DataFrame
    '''
    if report_date:
        # TODO 这里要做参数检查
        target_files_df = {"filename": [f"gpcw{i}.zip" for i in report_date]}  # 这里就暂时用字典伪装一下吧
    else:
        # 获取全部下载任务列表
        list_crawler = HistoryFinancialListCrawler()
        list_data = list_crawler.fetch_and_parse()
        target_files_df = pd.DataFrame(data=list_data)

    columns_list = financial_dict.values()
    result_df = pd.DataFrame(columns=columns_list)

    start_time = time.perf_counter()
    data_crawler = HistoryFinancialCrawler()
    pbar = tqdm(target_files_df['filename'])

    for filename in pbar:
        result = data_crawler.fetch_and_parse(
            # reporthook=demo_reporthook,
            filename=filename,
            path_to_download=f"./data/{filename}"
        )
        df = data_crawler.to_df(data=result)
        if df is None:
            continue
        df.reset_index(inplace=True)
        df.columns = columns_list
        result_df = result_df.append(df)
        pbar.set_description(f"{filename} loaded, result_df length: {len(result_df)}")
    print(f"Total download time cost:{time.perf_counter() - start_time:.2f}s")
    return result_df


if __name__ == '__main__':
    # df = download_financial_data()
    df = download_financial_data(report_date=["20200930", "20200630", "20200331", "20191231"])
    print(1)
    df.to_csv('financial_data.csv', index=False)

# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Datetime : 2020/10/19 17:03
# @Author   : Fangyang
# @Software : PyCharm

import time
from typing import List
import pandas as pd
from tqdm import tqdm
from pathlib import Path
from pytdx.crawler.history_financial_crawler import HistoryFinancialListCrawler, HistoryFinancialCrawler
from microservices.datasource.pytdx.financial.financial_mean import financial_dict


def download_financial_data(report_date: List[str] = None) -> pd.DataFrame:
    '''
    下载金融财务数据
    :param report_date: default None, 表示下载全部数据. 指定下载格式为 ["20200930", "20200630", "20200331", "20191231"], 其他格式和月日数字不行
    :return: 财务数据拼接的 DataFrame
    '''
    save_data_dir = Path(__file__).parent / "data"
    if not save_data_dir.exists():
        save_data_dir.mkdir()

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
    # 获取当前data文件下的.zip文件列表
    data_zip_file_list = [i.name for i in save_data_dir.glob("*.zip")]

    data_crawler = HistoryFinancialCrawler()
    pbar = tqdm(list(target_files_df['filename'].items()))

    for index, filename in pbar:
        target_file_size = target_files_df['filesize'][index]

        # 文件已经存在
        if filename in data_zip_file_list:
            exist_file_size = (save_data_dir / filename).stat().st_size
            # 如果已存在文件size小于目标文件, 重新下载新文件
            if exist_file_size < target_file_size*0.9999:
                pbar.set_description(f"{filename} need to update. Start download... {exist_file_size}/{target_file_size}")
                result = data_crawler.fetch_and_parse(
                    # reporthook=demo_reporthook,
                    filename=filename,
                    path_to_download=save_data_dir / filename
                )
            # 文件size满足, 直接读取本地文件
            else:
                pbar.set_description(f"Local {filename} loading...")
                with open(save_data_dir / filename, mode="rb") as f:
                    result = data_crawler.parse(f)
        # 文件不存在, 下载文件
        else:
            pbar.set_description(f"{filename} downloading...")
            result = data_crawler.fetch_and_parse(
                # reporthook=demo_reporthook,
                filename=filename,
                path_to_download=save_data_dir / filename
            )

        df = data_crawler.to_df(data=result)
        if df is None:
            continue
        df.reset_index(inplace=True)
        df.columns = columns_list

        # 这步省了, 可能是之前存csv的过程中0消失, 目前code为str
        # code列进行补0操作
        # df['code'] = df['code'].apply(lambda x: '{:0>6d}'.format(x))

        result_df = result_df.append(df)
        pbar.set_description(f"{filename} loaded, result_df length: {len(result_df)}")
    print(f"Total download time cost:{time.perf_counter() - start_time:.2f}s")
    return result_df


def save_df_to_influxdb():
    pass


def save_df_to_mongodb():
    pass


if __name__ == '__main__':
    df = download_financial_data()
    # df = download_financial_data(report_date=["20200930", "20200630", "20200331", "20191231"])
    print(1)
    df.to_csv('financial_data.csv', index=False)

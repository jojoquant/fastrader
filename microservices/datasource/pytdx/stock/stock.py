# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Datetime : 2020/10/19 13:33
# @Author   : Fangyang
# @Software : PyCharm
import time

import pandas as pd

import datetime
from pytdx.hq import TdxHq_API
from retrying import retry

from microservices.database.mongodb.pandas_opration import MongoDB
from microservices.datasource.pytdx.ips import IPsSource
from microservices.datasource.pytdx.stock.QAFetch.base import _select_market_code
from microservices.datasource.pytdx.stock.QAUtil.QADate import QA_util_date_stamp
from microservices.datasource.pytdx.stock.QAUtil.QADate_trade import QA_util_get_trade_gap


@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_get_stock_list(type_='stock', ip=None, port=None):
    if (ip is None) or (port is None):
        ips_pool = IPsSource()
        ip, port = ips_pool.get_fast_hq_ip()

    api = TdxHq_API()
    with api.connect(ip, port):
        data = pd.concat(
            [pd.concat([api.to_df(api.get_security_list(j, i * 1000)).assign(
                sse='sz' if j == 0 else 'sh').set_index(
                ['code', 'sse'], drop=False) for i in
                range(int(api.get_security_count(j) / 1000) + 1)], axis=0, sort=False) for
                j
                in range(2)], axis=0, sort=False)
        # data.code = data.code.apply(int)
        sz = data.query('sse=="sz"')
        sh = data.query('sse=="sh"')

        sz = sz.assign(sec=sz.code.apply(for_sz))
        sh = sh.assign(sec=sh.code.apply(for_sh))

        if type_ in ['stock', 'gp']:

            return pd.concat([sz, sh], sort=False).query(
                'sec=="stock_cn"').sort_index().assign(
                name=data['name'].apply(lambda x: str(x)[0:6]))

        elif type_ in ['index', 'zs']:

            return pd.concat([sz, sh], sort=False).query(
                'sec=="index_cn"').sort_index().assign(
                name=data['name'].apply(lambda x: str(x)[0:6]))
            # .assign(szm=data['name'].apply(lambda x: ''.join([y[0] for y in lazy_pinyin(x)])))\
            # .assign(quanpin=data['name'].apply(lambda x: ''.join(lazy_pinyin(x))))
        elif type_ in ['etf', 'ETF']:
            return pd.concat([sz, sh], sort=False).query(
                'sec=="etf_cn"').sort_index().assign(
                name=data['name'].apply(lambda x: str(x)[0:6]))

        else:
            return data.assign(
                code=data['code'].apply(lambda x: str(x))).assign(
                name=data['name'].apply(lambda x: str(x)[0:6]))
            # .assign(szm=data['name'].apply(lambda x: ''.join([y[0] for y in lazy_pinyin(x)])))\
            #    .assign(quanpin=data['name'].apply(lambda x: ''.join(lazy_pinyin(x))))


def for_sz(code):
    """深市代码分类
    Arguments:
        code {[type]} -- [description]
    Returns:
        [type] -- [description]
    """

    if str(code)[0:2] in ['00', '30', '02']:
        return 'stock_cn'
    elif str(code)[0:2] in ['39']:
        return 'index_cn'
    elif str(code)[0:2] in ['15']:
        return 'etf_cn'
    elif str(code)[0:3] in ['101', '104', '105', '106', '107', '108', '109',
                            '111', '112', '114', '115', '116', '117', '118', '119',
                            '123', '127', '128',
                            '131', '139', ]:
        # 10xxxx 国债现货
        # 11xxxx 债券
        # 12xxxx 可转换债券

        # 123
        # 127
        # 12xxxx 国债回购
        return 'bond_cn'

    elif str(code)[0:2] in ['20']:
        return 'stockB_cn'
    else:
        return 'undefined'


def for_sh(code):
    if str(code)[0] == '6':
        return 'stock_cn'
    elif str(code)[0:3] in ['000', '880']:
        return 'index_cn'
    elif str(code)[0:2] == '51':
        return 'etf_cn'
    # 110×××120×××企业债券；
    # 129×××100×××可转换债券；
    # 113A股对应可转债 132
    elif str(code)[0:3] in ['102', '110', '113', '120', '122', '124',
                            '130', '132', '133', '134', '135', '136',
                            '140', '141', '143', '144', '147', '148']:
        return 'bond_cn'
    else:
        return 'undefined'


@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_get_stock_day(code, start_date, end_date, if_fq='00',
                           frequence='day', ip=None, port=None):
    """获取日线及以上级别的数据
    Arguments:
        code {str:6} -- code 是一个单独的code 6位长度的str
        start_date {str:10} -- 10位长度的日期 比如'2017-01-01'
        end_date {str:10} -- 10位长度的日期 比如'2018-01-01'
    Keyword Arguments:
        if_fq {str} -- '00'/'bfq' -- 不复权 '01'/'qfq' -- 前复权 '02'/'hfq' -- 后复权 '03'/'ddqfq' -- 定点前复权 '04'/'ddhfq' --定点后复权
        frequency {str} -- day/week/month/quarter/year 也可以是简写 D/W/M/Q/Y
        ip {str} -- [description] (default: None) ip可以通过select_best_ip()函数重新获取
        port {int} -- [description] (default: {None})
    Returns:
        pd.DataFrame/None -- 返回的是dataframe,如果出错比如只获取了一天,而当天停牌,返回None
                            column : ochl + vol + amount + date + code + date_stamp
    Exception:
        如果出现网络问题/服务器拒绝, 会出现socket:time out 尝试再次获取/更换ip即可, 本函数不做处理
    """
    if (ip is None) or (port is None):
        ips_pool = IPsSource()
        ip, port = ips_pool.get_fast_hq_ip()

    api = TdxHq_API()
    try:
        with api.connect(ip, port, time_out=0.7):

            if frequence in ['day', 'd', 'D', 'DAY', 'Day']:
                frequence = 9
            elif frequence in ['w', 'W', 'Week', 'week']:
                frequence = 5
            elif frequence in ['month', 'M', 'm', 'Month']:
                frequence = 6
            elif frequence in ['quarter', 'Q', 'Quarter', 'q']:
                frequence = 10
            elif frequence in ['y', 'Y', 'year', 'Year']:
                frequence = 11
            start_date = str(start_date)[0:10]
            today_ = datetime.date.today()
            lens = QA_util_get_trade_gap(start_date, today_)

            data = pd.concat([api.to_df(
                api.get_security_bars(frequence, _select_market_code(
                    code), code, (int(lens / 800) - i) * 800, 800)) for i in
                range(int(lens / 800) + 1)], axis=0, sort=False)

            # 这里的问题是: 如果只取了一天的股票,而当天停牌, 那么就直接返回None了
            if len(data) < 1:
                return None
            data = data[data['open'] != 0]

            data = data.assign(
                date=data['datetime'].apply(lambda x: str(x[0:10])),
                code=str(code),
                date_stamp=data['datetime'].apply(
                    lambda x: QA_util_date_stamp(str(x)[0:10]))) \
                .set_index('date', drop=False, inplace=False)

            end_date = str(end_date)[0:10]
            data = data.drop(
                ['year', 'month', 'day', 'hour', 'minute', 'datetime'],
                axis=1)[
                   start_date:end_date]
            if if_fq in ['00', 'bfq']:
                return data
            else:
                print('CURRENTLY NOT SUPPORT REALTIME FUQUAN')
                return None
                # xdxr = QA_fetch_get_stock_xdxr(code)
                # if if_fq in ['01','qfq']:
                #     return QA_data_make_qfq(data,xdxr)
                # elif if_fq in ['02','hfq']:
                #     return QA_data_make_hfq(data,xdxr)
    except Exception as e:
        if isinstance(e, TypeError):
            print('Tushare内置的pytdx版本和QUANTAXIS使用的pytdx 版本不同, 请重新安装pytdx以解决此问题')
            print('pip uninstall pytdx')
            print('pip install pytdx')
        else:
            print(e)


if __name__ == '__main__':
    code = '000001'

    ip = "39.98.198.249"
    port = 7709
    # df1 = QA_fetch_get_stock_list(ip=ip, port=port)
    stock_df = QA_fetch_get_stock_day(code=code, start_date="1990-01-01", end_date="2019-12-25", ip=ip, port=port)
    stock_df['date'] = pd.to_datetime(stock_df['date'], format='%Y-%m-%d', utc=False)
    stock_df['date'] = stock_df['date'].dt.tz_localize('Asia/Shanghai')  # 设置当前时间为东八区
    stock_df.reset_index(drop=True, inplace=True)

    pd_mongo = MongoDB()
    financial_df = pd_mongo.read_db(
        query=(
            {
                "code": code,
                # "totalCapital": {"$ne": 0},
            },
            {"_id": 0, "code": 1, "report_date": 1, "totalCapital": 1, "totalShare":1, "totalOwnersEquity":1}
        )
    )
    financial_df['report_date'] = financial_df['report_date'].dt.tz_localize('UTC')  # 设置当前时间为东八区
    financial_df['report_date'] = financial_df['report_date'].dt.tz_convert('Asia/Shanghai')  # 转成utc时间
    financial_df.rename(columns={"report_date": "date"}, inplace=True)

    start_time = time.perf_counter()
    stock_merge_df = stock_df.merge(financial_df, how="left").fillna(method="bfill").fillna(method="ffill")
    print(f"Merge cost: {time.perf_counter() - start_time:.2f}s")
    stock_merge_df["close*totalShare"] = stock_merge_df["close"]*stock_merge_df["totalShare"]
    stock_merge_df["close*totalCapital"] = stock_merge_df["close"]*stock_merge_df["totalCapital"]

    stock_merge_df.to_csv("stock_merge.csv", index=False)
    print(1)

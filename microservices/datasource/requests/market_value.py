# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Datetime : 2020/10/19 13:08
# @Author   : Fangyang
# @Software : PyCharm
import json
import pandas as pd
import requests

# market_value_url = "https://eniu.com/gu/sh600000/market_value"
market_value_url = "https://eniu.com/chart/marketvaluea/sh600000"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
}
res = requests.get(url=market_value_url, headers=headers)
res_dict = json.loads(res.text)
res_df = pd.DataFrame(res_dict)
print(1)

if __name__ == '__main__':
    pass

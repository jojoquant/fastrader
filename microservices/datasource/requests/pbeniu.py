# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Datetime : 2020/10/8 0:54
# @Author   : Fangyang
# @Software : PyCharm
import json
import pandas as pd
import requests


code = "sz000001"
pe_url = f"https://eniu.com/chart/pea/{code}"
pb_url = f"https://eniu.com/chart/pba/{code}"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
}
pb_res = requests.get(url=pb_url, headers=headers)
pe_res = requests.get(url=pe_url, headers=headers)
pb_df = pd.DataFrame(json.loads(pb_res.text))
pe_df = pd.DataFrame(json.loads(pe_res.text))

pe_df['pe/pb'] = pe_df['pe_ttm']/pb_df['pb']
pe_df['pb'] = pb_df['pb']
pe_df['e'] = pe_df['price']/pe_df['pe_ttm']
for i in [13, 48]:
    pe_df[f'{i}e'] = pe_df['e'] * i

pe_df.to_csv("pepb.csv", index=False)
print(1)

if __name__ == '__main__':
    pass

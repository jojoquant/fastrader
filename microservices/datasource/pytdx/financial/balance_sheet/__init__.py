# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Datetime : 2020/10/19 22:59
# @Author   : Fangyang
# @Software : PyCharm

from microservices.datasource.pytdx.financial.balance_sheet.assets import assets_dict
from microservices.datasource.pytdx.financial.balance_sheet.liabilities import liabilities_dict
from microservices.datasource.pytdx.financial.balance_sheet.equity import owner_equity_dict

balance_sheet_dict = {
    # 2. 资产负债表 BALANCE SHEET
    # 2.1 资产
    **assets_dict,
    # 2.2 负债
    **liabilities_dict,
    # 2.3 所有者权益
    **owner_equity_dict,
    '073负债和所有者（或股东权益）合计': 'totalLiabilitiesAndOwnersEquity',
}

if __name__ == '__main__':
    pass

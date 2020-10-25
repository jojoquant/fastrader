# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Datetime : 2020/10/20 2:19
# @Author   : Fangyang
# @Software : PyCharm


from microservices.datasource.pytdx.financial.fundamental_analysis.solvency import solvency_dict
from microservices.datasource.pytdx.financial.fundamental_analysis.operating_capability import operating_capability_dict
from microservices.datasource.pytdx.financial.fundamental_analysis.growth_capability import growth_capability_dict
from microservices.datasource.pytdx.financial.fundamental_analysis.profitability import profitability_dict
from microservices.datasource.pytdx.financial.fundamental_analysis.capital_structure import capital_structure_dict
from microservices.datasource.pytdx.financial.fundamental_analysis.cash_capability import cash_capability_dict

fundamental_analysis_dict = {
    # 5. 偿债能力分析
    **solvency_dict,
    # 6. 经营效率分析
    **operating_capability_dict,
    # 7. 发展能力分析
    **growth_capability_dict,
    # 8. 获利能力分析
    **profitability_dict,
    # 9. 资本结构分析
    **capital_structure_dict,
    # 10. 现金流量分析
    **cash_capability_dict
}

if __name__ == '__main__':
    pass

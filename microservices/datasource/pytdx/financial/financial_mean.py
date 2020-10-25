# coding:utf-8

from microservices.datasource.pytdx.financial.balance_sheet import balance_sheet_dict
from microservices.datasource.pytdx.financial.income_statement import income_statement_dict
from microservices.datasource.pytdx.financial.cash_flow_statement import cash_flow_statement_dict
from microservices.datasource.pytdx.financial.fundamental_analysis import fundamental_analysis_dict

from microservices.datasource.pytdx.financial.unknown import unknown_dict

info_per_share_dict = {
    # 1.每股指标
    '000股票代码': 'code',
    '000报告日期': 'report_date',
    '001基本每股收益': 'EPS',
    '002扣除非经常性损益每股收益': 'deductEPS',
    '003每股未分配利润': 'undistributedProfitPerShare',
    '004每股净资产': 'netAssetsPerShare',
    '005每股资本公积金': 'capitalReservePerShare',
    '006净资产收益率': 'ROE',
    '007每股经营现金流量': 'operatingCashFlowPerShare1',
}

financial_dict = {
    # 1.每股指标 0~7
    **info_per_share_dict,
    # 资产负债表 8~73
    **balance_sheet_dict,
    # 利润表 74~97
    **income_statement_dict,
    # 现金流量表 98~158
    **cash_flow_statement_dict,
    # 基本面分析 159~229
    **fundamental_analysis_dict,

    # 11. 单季度财务指标
    '230营业收入': 'operatingRevenueSingle',
    '231营业利润': 'operatingProfitSingle',
    '232归属于母公司所有者的净利润': 'netProfitBelongingToTheOwnerOfTheParentCompanySingle',
    '233扣除非经常性损益后的净利润': 'netProfitAfterExtraordinaryGainsAndLossesSingle',
    '234经营活动产生的现金流量净额': 'netCashFlowsFromOperatingActivitiesSingle',
    '235投资活动产生的现金流量净额': 'netCashFlowsFromInvestingActivitiesSingle',
    '236筹资活动产生的现金流量净额': 'netCashFlowsFromFinancingActivitiesSingle',
    '237现金及现金等价物净增加额': 'netIncreaseInCashAndCashEquivalentsSingle',
    # 12.股本股东
    '238总股本': 'totalCapital',
    '239已上市流通A股': 'listedAShares',
    '240已上市流通B股': 'listedBShares',
    '241已上市流通H股': 'listedHShares',
    '242股东人数(户)': 'numberOfShareholders',
    '243第一大股东的持股数量': 'theNumberOfFirstMajorityShareholder',
    '244十大流通股东持股数量合计(股)': 'totalNumberOfTopTenCirculationShareholdersAB',
    '245十大股东持股数量合计(股)': 'totalNumberOfTopTenMajorShareholders',
    # 13.机构持股
    '246机构总量（家）': 'institutionNumber',
    '247机构持股总量(股)': 'institutionShareholding',
    '248QFII机构数': 'QFIIInstitutionNumber',
    '249QFII持股量': 'QFIIShareholding',
    '250券商机构数': 'brokerNumber',
    '251券商持股量': 'brokerShareholding',
    '252保险机构数': 'securityNumber',
    '253保险持股量': 'securityShareholding',
    '254基金机构数': 'fundsNumber',
    '255基金持股量': 'fundsShareholding',
    '256社保机构数': 'socialSecurityNumber',
    '257社保持股量': 'socialSecurityShareholding',
    '258私募机构数': 'privateEquityNumber',
    '259私募持股量': 'privateEquityShareholding',
    '260财务公司机构数': 'financialCompanyNumber',
    '261财务公司持股量': 'financialCompanyShareholding',
    '262年金机构数': 'pensionInsuranceAgencyNumber',
    '263年金持股量': 'pensionInsuranceAgencyShareholfing',
    # 14.新增指标
    # [注：季度报告中，若股东同时持有非流通A股性质的股份(如同时持有流通A股和流通B股），取的是包含同时持有非流通A股性质的流通股数]
    '264十大流通股东中持有A股合计(股)': 'totalNumberOfTopTenCirculationShareholdersA',
    '265第一大流通股东持股量(股)': 'firstLargeCirculationShareholdersNumber',
    # [注：1.自由流通股=已流通A股-十大流通股东5%以上的A股；2.季度报告中，若股东同时持有非流通A股性质的股份(如同时持有流通A股和流通H股），5%以上的持股取的是不包含同时持有非流通A股性质的流通股数，结果可能偏大； 3.指标按报告期展示，新股在上市日的下个报告期才有数据]
    '266自由流通股(股)': 'freeCirculationStock',
    '267受限流通A股(股)': 'limitedCirculationAShares',
    '268一般风险准备(金融类)': 'generalRiskPreparation',
    '269其他综合收益(利润表)': 'otherComprehensiveIncome',
    '270综合收益总额(利润表)': 'totalComprehensiveIncome',
    '271归属于母公司股东权益(资产负债表)': 'shareholdersOwnershipOfAParentCompany',
    '272银行机构数(家)(机构持股)': 'bankInstutionNumber',
    '273银行持股量(股)(机构持股)': 'bankInstutionShareholding',
    '274一般法人机构数(家)(机构持股)': 'corporationNumber',
    '275一般法人持股量(股)(机构持股)': 'corporationShareholding',
    '276近一年净利润(元)': 'netProfitLastYear',
    '277信托机构数(家)(机构持股)': 'trustInstitutionNumber',
    '278信托持股量(股)(机构持股)': 'trustInstitutionShareholding',
    '279特殊法人机构数(家)(机构持股)': 'specialCorporationNumber',
    '280特殊法人持股量(股)(机构持股)': 'specialCorporationShareholding',
    '281加权净资产收益率(每股指标)': 'weightedROE',
    '282扣非每股收益(单季度财务指标)': 'nonEPSSingle',
    '283最近一年营业收入(万元)': 'lastYearOperatingIncome',
    '284国家队持股数量(万股)': 'nationalTeamShareholding',
    # [注：本指标统计包含汇金公司、证金公司、外汇管理局旗下投资平台、国家队基金、国开、养老金以及中科汇通等国家队机构持股数量]
    '285业绩预告-本期净利润同比增幅下限%': 'PF_theLowerLimitoftheYearonyearGrowthofNetProfitForThePeriod',
    # [注：指标285至294展示未来一个报告期的数据。例，3月31日至6月29日这段时间内展示的是中报的数据；如果最新的财务报告后面有多个报告期的业绩预告/快报，只能展示最新的财务报告后面的一个报告期的业绩预告/快报]
    '286业绩预告-本期净利润同比增幅上限%': 'PF_theHigherLimitoftheYearonyearGrowthofNetProfitForThePeriod',
    '287业绩快报-归母净利润': 'PE_returningtotheMothersNetProfit',
    '288业绩快报-扣非净利润': 'PE_Non-netProfit',
    '289业绩快报-总资产': 'PE_TotalAssets',
    '290业绩快报-净资产': 'PE_NetAssets',
    '291业绩快报-每股收益': 'PE_EPS',
    '292业绩快报-摊薄净资产收益率': 'PE_DilutedROA',
    '293业绩快报-加权净资产收益率': 'PE_WeightedROE',
    '294业绩快报-每股净资产': 'PE_NetAssetsperShare',
    '295应付票据及应付账款(资产负债表)': 'BS_NotesPayableandAccountsPayable',
    '296应收票据及应收账款(资产负债表)': 'BS_NotesReceivableandAccountsReceivable',
    '297递延收益(资产负债表)': 'BS_DeferredIncome',
    '298其他综合收益(资产负债表)': 'BS_OtherComprehensiveIncome',
    '299其他权益工具(资产负债表)': 'BS_OtherEquityInstruments',
    '300其他收益(利润表)': 'IS_OtherIncome',
    '301资产处置收益(利润表)': 'IS_AssetDisposalIncome',
    '302持续经营净利润(利润表)': 'IS_NetProfitforContinuingOperations',
    '303终止经营净利润(利润表)': 'IS_NetProfitforTerminationOperations',
    '304研发费用(利润表)': 'IS_R&DExpense',
    '305其中:利息费用(利润表-财务费用)': 'IS_InterestExpense',
    '306其中:利息收入(利润表-财务费用)': 'IS_InterestIncome',
    '307近一年经营活动现金流净额': 'netCashFlowfromOperatingActivitiesinthepastyear',
    **unknown_dict,
}

if __name__ == "__main__":
    pass

# -*- coding:utf-8 -*-
#策略选择工具
from stockbaseinfo.strategy.utils import *

#选择净利润较好的公司
def getBestProfit():
    dictIndexDateIsCow = {}
    setCowSql = '''SELECT `code`, `subject_title`,`account1`,`account2`,`account3`,`account4`,`account5`, `account6`, `account7`, `account8`, `account9`, `account10`,
    `year1`,`year2`,`year3`,`year4`,`year5`,`year6`,`year7`,`year8`,`year9`,`year10`,`season` FROM  `main_index` where subject_title like '%净利润增长率%' order by code,season ;'''
    lstitem = Utils.fetch_data(setCowSql)
    for item in lstitem:
        print(item)
    #     tempcodename = ''
    #     tempdateiscow = ''
    #     code = item[0]
    #     name = item[1]
    #     iscow = item[2]
    #     sdate = item[3]
    #     tempcodename = code + ',' + name
    #     tempdateiscow = str(sdate) + ':' + str(iscow)
    #     if dictIndexDateIsCow.__contains__(tempcodename):
    #         # codedata = dictIndexDateIsCow[tempcodename]
    #         dictIndexDateIsCow[tempcodename] += tempdateiscow + ','
    #     else:
    #         dictIndexDateIsCow[tempcodename] = ''
    # print('----------------------------判断熊市牛市---------------------------------------------------------')
    # for key, value in dictIndexDateIsCow.items():
    #     print(key + "---" + value)
    # print('****************************判断熊市牛市********************************************************')

def getUprise():
    lstOri = [3,4,5,6,5,4,3,22,1,2,3,4,5,6,7,8,9,7,6,5,4,6,8,9,10]
    lastMaxP = 0
    lastMinP = 0
    lstMax=[]
    lstMin = []
    lstMaxData=[]
    lstMinData=[]
    lstOri.reverse()
    for i in range(len(lstOri)):
        if i == 0:
            pass
        else:
            minp = min(lstOri[0:i])
            if minp<lastMinP:
                lastMinP = minp
            else:
                if lstMinData.count(minp)<1:
                    lstMin.append(str(i)+":"+str(minp))
                    lstMinData.append(minp)

    for mindata in lstMin:
        print(mindata)

#计算所有股票在每一个交易日的向前120日滚动RPS值。对股票价格走势和RPS进行可视化
# 欧奈尔研究了1953年至1993年，500只年度涨幅最大的股票，发现每年涨幅居前的，在他们股价真正大幅度攀升之前，其平均的相对强弱指标RPS为87％。这并不意味着，只要RPS>87%就可以买入该股票呢？其实RPS指标只是对强势股的个一个初步筛选，对于A股而言，RPS大于87%的股票就有400多只，都买进也不太现实，具体运用还需结合个股基本面、题材和整体市场情况分析。RPS实际上是欧奈尔在《笑傲股市》中提出的CANSLIM七步选股法的一个技术分析。各字母含义如下所示：C：最近一季度报表显示的盈利（每股收益）
# A：每年度每股盈利的增长幅度
# N：新产品，新服务，股价创新高
# S：该股流通盘大小，市值以及交易量的情况
# L：该股票在行业中的低位，是否为龙头
# I：该股票有无有实力的庄家，机构大流通股东
# M：大盘走势如何，如何判断大盘走向
#
# RPS英文全称Relative Price Strength Rating，即股价相对强度，该指标是欧奈尔CANSLIM选股法则中的趋势分析，具有很强的实战指导意义。RPS指标是指在一段时间内，个股涨幅在全部股票涨幅排名中的位次值。
# 比如A股共有3500只股票，若某只股票的120日涨幅在所有股票中排名第350位，则该股票的RPS值为：(1-350/3500)*100=90。
#
# RPS的值代表该股的120日涨幅超过其他90%的股票的涨幅。通过该指标可以反映个股股价走势在同期市场中的表现相对强弱。RPS的值介于0-100之间，在过去的一年中，所有股票的涨幅排行中，前1%的股票的RPS值为99至100，前2%的股票的RPS值为98至99，以此类推。RPS时间周期可以自己根据需要进行调整，常用的有60日（3个月）、120日（半年）和250日（一年）等。

def getRPS120():
    print()
if __name__ == "__main__":
    getUprise()
    # data = "1:23"
    # print(data[:data.index(":")])
# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from stockbaseinfo.items import *
from stockbaseinfo.Const import *
from stockbaseinfo.utils import *
import json
import requests


#需要处理的几个事情：
#1.需要支持多个连接组成的访问群组，而且需要不同的顺序完成
#2.需要支持一个yeild来封装不同数据类型
#3.参考这个网址 完成剩下的内容：https://www.jianshu.com/p/6740c83e4540
#4.用来获取基本信息 http://api.cninfo.com.cn/v5/hq/dataItem?codelist=sh603158

#TODO:需要统一处理数据不足10个的情况，需要设计一个方案来接收这些数据

class BaseinfoSpider(scrapy.Spider):
    name = 'baseinfo'
    # allowed_domains = ['zyh.com']
    start_urls = ['http://www.cninfo.com.cn/new/disclosure/stock?orgId=9900026564&stockCode=002796']

    def start_requests(self):
        for code in Const.LST_S_CODE:
            tsurl = Const.BASEINFO_URL + code
            yield scrapy.Request(tsurl,callback=self.info_parse)
        for code in Const.LST_CODE:
            para = 'scode=' + code
            data1 = {
                'mergerMark': 'sysapi1067', 'paramStr': para
            }
            yield scrapy.FormRequest(Const.DATAINFO_URL,formdata=data1, method='POST',callback=self.parse)

    #解析其他信息
    def parse(self, response):
        print('--------------profit_parse-----------------------------')
        if len(response.text) > 4:
            js = json.loads(response.text)
            code = js[0]['SECCODE']
            param = js[0]['F002N']
            #---------------------------------------请求资产负债表--------------------------------------------------------------
            para = 'scode=' + code + ';rtype=1;sign=' + str(param)
            # 资产负债表
            balance_data = {
                'mergerMark': 'sysapi1077', 'paramStr': para
            }
            yield scrapy.FormRequest(Const.DATAINFO_URL, formdata=balance_data, method='POST', callback=lambda response,code=code:self.balance_parse(response,code))
            # *************************************请求资产负债表**************************************************************

            #---------------------------------------请求利润表--------------------------------------------------------------
            #一季度利润表
            para = 'scode=' + code + ';rtype=1;sign=' + str(param)
            profit_data = {
                'mergerMark': 'sysapi1075', 'paramStr': para
            }
            yield scrapy.FormRequest(Const.DATAINFO_URL, formdata=profit_data, method='POST',callback=lambda response,code=code,rtype='1':self.profit_parse(response,code,rtype))
            #半年利润表
            para = 'scode=' + code + ';rtype=2;sign=' + str(param)
            profit_data = {
                'mergerMark': 'sysapi1075', 'paramStr': para
            }
            yield scrapy.FormRequest(Const.DATAINFO_URL, formdata=profit_data, method='POST', callback=lambda response,code=code,rtype='2':self.profit_parse(response,code,rtype))
            #三季度利润表
            para = 'scode=' + code + ';rtype=3;sign=' + str(param)
            profit_data = {
                'mergerMark': 'sysapi1075', 'paramStr': para
            }
            yield scrapy.FormRequest(Const.DATAINFO_URL, formdata=profit_data, method='POST', callback=lambda response,code=code,rtype='3':self.profit_parse(response,code,rtype))
            #年度利润表
            para = 'scode=' + code + ';rtype=4;sign=' + str(param)
            profit_data = {
                'mergerMark': 'sysapi1075', 'paramStr': para
            }
            yield scrapy.FormRequest(Const.DATAINFO_URL, formdata=profit_data, method='POST', callback=lambda response,code=code,rtype='4':self.profit_parse(response,code,rtype))
            # *************************************请求利润表**************************************************************
            #---------------------------------------请求现金流量表--------------------------------------------------------------
            para = 'scode=' + code + ';rtype=1;sign=' + str(param)
            cashflow_data = {
                'mergerMark': 'sysapi1076', 'paramStr': para
            }
            yield scrapy.FormRequest(Const.DATAINFO_URL, formdata=cashflow_data, method='POST', callback=lambda response,code=code:self.cashflow_parse(response,code))
            # *************************************请求现金流量表**************************************************************
            #---------------------------------------请求历史分红表--------------------------------------------------------------
            para = 'scode=' + code
            # 分红
            bonus_data = {
                'mergerMark': 'sysapi1073', 'paramStr': para
            }
            yield scrapy.FormRequest(Const.DATAINFO_URL, formdata=bonus_data, method='POST', callback=lambda response,code=code:self.bonus_parse(response,code))
            # *************************************请求历史分红表**************************************************************
            #---------------------------------------请求主要指标表--------------------------------------------------------------
            para = 'scode=' + code + ';rtype=1'
            mainindex_data = {
                'mergerMark': 'sysapi1074', 'paramStr': para
            }
            yield scrapy.FormRequest(Const.DATAINFO_URL, formdata=mainindex_data, method='POST', callback=lambda response,code=code,rtype='1':self.mainindex_parse(response,code,rtype))
            para = 'scode=' + code + ';rtype=2'
            mainindex_data = {
                'mergerMark': 'sysapi1074', 'paramStr': para
            }
            yield scrapy.FormRequest(Const.DATAINFO_URL, formdata=mainindex_data, method='POST',
                                     callback=lambda response, code=code, rtype='2': self.mainindex_parse(response, code,
                                                                                                          rtype))
            para = 'scode=' + code + ';rtype=3'
            mainindex_data = {
                'mergerMark': 'sysapi1074', 'paramStr': para
            }
            yield scrapy.FormRequest(Const.DATAINFO_URL, formdata=mainindex_data, method='POST',
                                     callback=lambda response, code=code, rtype='3': self.mainindex_parse(response, code,
                                                                                                          rtype))
            para = 'scode=' + code + ';rtype=4'
            mainindex_data = {
                'mergerMark': 'sysapi1074', 'paramStr': para
            }
            yield scrapy.FormRequest(Const.DATAINFO_URL, formdata=mainindex_data, method='POST',
                                     callback=lambda response, code=code, rtype='4': self.mainindex_parse(response, code,
                                                                                                          rtype))
            # *************************************请求主要指标表**************************************************************
            # ---------------------------------------请求十大流通股东--------------------------------------------------------------
            para = 'scode=' + code
            # 十大股东
            holders_data = {
                'mergerMark': 'sysapi1071', 'paramStr': para
            }
            yield scrapy.FormRequest(Const.DATAINFO_URL, formdata=holders_data, method='POST',callback=lambda response,code=code:self.holders_parse(response,code))
            # *************************************请求十大流通股东**************************************************************

    def profit_parse(self, response,code,rtype):
        print('--------------profit_parse-----------------------------')
        if len(response.text) > 4:
            data = json.loads(response.text)
            lst_profit = []
            for item in data:
                subject_title = item['index']
                lstyear = list(item.keys())
                lstyear.remove('index')
                lstyear.sort()
                if len(lstyear) == 10:
                    profitsheet_item = profit_sheetItem(code, subject_title,rtype, item[lstyear[0]], item[lstyear[1]],
                                                           item[lstyear[2]], item[lstyear[3]], item[lstyear[4]],
                                                           item[lstyear[5]], item[lstyear[6]],
                                                           item[lstyear[7]], item[lstyear[8]], item[lstyear[9]],
                                                           lstyear[0], lstyear[1], lstyear[2], lstyear[3], lstyear[4],
                                                           lstyear[5],
                                                           lstyear[6], lstyear[7], lstyear[8], lstyear[9])
                    lst_profit.append(profitsheet_item)
                elif len(lstyear) > 0:
                    arr_inityear, arr_initdata = Utils.load_validdata(lstyear, item)
                    if len(arr_inityear) > 0 and len(arr_initdata) > 0:
                        profitsheet_item = profit_sheetItem(code, subject_title, rtype, arr_initdata[0], arr_initdata[1],
                                                               arr_initdata[2], arr_initdata[3], arr_initdata[4],
                                                               arr_initdata[5], arr_initdata[6],
                                                               arr_initdata[7], arr_initdata[8], arr_initdata[9],
                                                               arr_inityear[0], arr_inityear[1], arr_inityear[2],
                                                               arr_inityear[3],
                                                               arr_inityear[4], arr_inityear[5],
                                                               arr_inityear[6], arr_inityear[7], arr_inityear[8],
                                                               arr_inityear[9])
                        lst_profit.append(profitsheet_item)
            stockbaseinfoitme = StockbaseinfoItem()
            stockbaseinfoitme['data_type'] = Const.PROFIT_SHEET
            stockbaseinfoitme['data_content'] = lst_profit
            yield stockbaseinfoitme
        print('-----------end---profit_parse-----------------------------')
    def balance_parse(self, response,code):
        print('--------------balance_parse-----------------------------')
        if len(response.text) > 4:
            data = json.loads(response.text)
            lst_blance_sheet = []
            for item in data:
                if item['index'].find('科目')>0:
                    pass;
                else:
                    subject_title = item['index']
                    lstyear = list(item.keys())
                    lstyear.remove('index')
                    lstyear.sort()
                    if len(lstyear) == 10:
                        balance_sheet_item=balance_sheetItem(code,subject_title,item[lstyear[0]],item[lstyear[1]],item[lstyear[2]],item[lstyear[3]],item[lstyear[4]],item[lstyear[5]],item[lstyear[6]],
                                                             item[lstyear[7]],item[lstyear[8]],item[lstyear[9]],lstyear[0],lstyear[1],lstyear[2],lstyear[3],lstyear[4],lstyear[5],
                                                             lstyear[6],lstyear[7],lstyear[8],lstyear[9])
                        lst_blance_sheet.append(balance_sheet_item)
                    elif len(lstyear)>0:
                        arr_inityear,arr_initdata = Utils.load_validdata(lstyear,item)
                        if len(arr_inityear)>0 and len(arr_initdata)>0:
                            balance_sheet_item = balance_sheetItem(code, subject_title, arr_initdata[0], arr_initdata[1],
                                                                   arr_initdata[2], arr_initdata[3], arr_initdata[4],
                                                                   arr_initdata[5], arr_initdata[6],
                                                                   arr_initdata[7], arr_initdata[8], arr_initdata[9],
                                                                   arr_inityear[0], arr_inityear[1], arr_inityear[2], arr_inityear[3],
                                                                   arr_inityear[4], arr_inityear[5],
                                                                   arr_inityear[6], arr_inityear[7], arr_inityear[8], arr_inityear[9])
                            lst_blance_sheet.append(balance_sheet_item)
            stockbaseinfoitme = StockbaseinfoItem()
            stockbaseinfoitme['data_type'] = Const.BALANCE_SHEET
            stockbaseinfoitme['data_content'] = lst_blance_sheet
            yield stockbaseinfoitme
        print('-----------end---balance_parse-----------------------------')
    def mainindex_parse(self,response,code,rtype):
        print('--------------mainindex_parse-----------------------------')
        if len(response.text) > 4:
            data = json.loads(response.text)
            lst_mainindex = []
            for item in data:
                subject_title = item['index']
                lstyear = list(item.keys())
                lstyear.remove('index')
                lstyear.sort()
                if len(lstyear) == 10:
                    mainindex_item = main_indexItem(code, subject_title, rtype, item[lstyear[0]], item[lstyear[1]],
                                                    item[lstyear[2]], item[lstyear[3]], item[lstyear[4]],
                                                    item[lstyear[5]], item[lstyear[6]],
                                                    item[lstyear[7]], item[lstyear[8]], item[lstyear[9]],
                                                    lstyear[0], lstyear[1], lstyear[2], lstyear[3], lstyear[4],
                                                    lstyear[5],
                                                    lstyear[6], lstyear[7], lstyear[8], lstyear[9])
                    lst_mainindex.append(mainindex_item)
                elif len(lstyear) > 0:
                    arr_inityear, arr_initdata = Utils.load_validdata(lstyear, item)
                    mainindex_item = main_indexItem(code, subject_title,rtype,arr_initdata[0], arr_initdata[1],
                                                                   arr_initdata[2], arr_initdata[3], arr_initdata[4],
                                                                   arr_initdata[5], arr_initdata[6],
                                                                   arr_initdata[7], arr_initdata[8], arr_initdata[9],
                                                                   arr_inityear[0], arr_inityear[1], arr_inityear[2], arr_inityear[3],
                                                                   arr_inityear[4], arr_inityear[5],
                                                                   arr_inityear[6], arr_inityear[7], arr_inityear[8], arr_inityear[9])
                    lst_mainindex.append(mainindex_item)
            stockbaseinfoitme = StockbaseinfoItem()
            stockbaseinfoitme['data_type'] = Const.MAIN_INDEX
            stockbaseinfoitme['data_content'] = lst_mainindex
            yield stockbaseinfoitme
        print('-----------end---mainindex_parse-----------------------------')

    def cashflow_parse(self, response,code):
        print('--------------cashflow_parse-----------------------------')
        if len(response.text) > 4:
            data = json.loads(response.text)
            lst_cashflow = []
            for item in data:
                subject_title = item['index']
                lstyear = list(item.keys())
                lstyear.remove('index')
                lstyear.sort()
                if len(lstyear) == 10:
                    cashflow_item = cash_flowItem(code, subject_title, item[lstyear[0]], item[lstyear[1]],
                                                           item[lstyear[2]], item[lstyear[3]], item[lstyear[4]],
                                                           item[lstyear[5]], item[lstyear[6]],
                                                           item[lstyear[7]], item[lstyear[8]], item[lstyear[9]],
                                                           lstyear[0], lstyear[1], lstyear[2], lstyear[3], lstyear[4],
                                                           lstyear[5],
                                                           lstyear[6], lstyear[7], lstyear[8], lstyear[9])
                    lst_cashflow.append(cashflow_item)
                elif len(lstyear) > 0:
                    arr_inityear, arr_initdata = Utils.load_validdata(lstyear, item)
                    if len(arr_inityear) > 0 and len(arr_initdata) > 0:
                        cashflow_item = cash_flowItem(code, subject_title, arr_initdata[0], arr_initdata[1],
                                                               arr_initdata[2], arr_initdata[3], arr_initdata[4],
                                                               arr_initdata[5], arr_initdata[6],
                                                               arr_initdata[7], arr_initdata[8], arr_initdata[9],
                                                               arr_inityear[0], arr_inityear[1], arr_inityear[2],
                                                               arr_inityear[3],
                                                               arr_inityear[4], arr_inityear[5],
                                                               arr_inityear[6], arr_inityear[7], arr_inityear[8],
                                                               arr_inityear[9])
                        lst_cashflow.append(cashflow_item)
            stockbaseinfoitme = StockbaseinfoItem()
            stockbaseinfoitme['data_type'] = Const.CASH_FLOW
            stockbaseinfoitme['data_content'] = lst_cashflow
            yield stockbaseinfoitme
        print('-----------end---cashflow_parse-----------------------------')
    def holders_parse(self,response,code):
        print('--------------holders_parse-----------------------------')
        if len(response.text) > 4:
            data = json.loads(response.text)
            lst_stockholders = []
            for item in data:
                stockholder_item = stock_holdersItem(code,item['F005N'],item['F002V'],item['F003N'],item['F004N'],item['F006V'],item['F001D'])
                lst_stockholders.append(stockholder_item)
            stockbaseinfoitme = StockbaseinfoItem()
            stockbaseinfoitme['data_type'] = Const.STOCK_HOLDERS
            stockbaseinfoitme['data_content'] = lst_stockholders
            yield stockbaseinfoitme
        print('-----------end---holders_parse-----------------------------')

    def bonus_parse(self, response,code):
        print('--------------bonus_parse-----------------------------')
        if len(response.text) > 4:
            data = json.loads(response.text)
            lst_bonus = []
            for item in data:
                notice_date = item['F013D']
                rightoff_time = item['F014D']
                stock_right_registe_date = item['F015D']
                cash_per_share = item['F010N']
                send_bonus_share_per_share = item['F012N']
                increase_shares_per_share = item['F011N']
                cash_receive_date = item['F016D']
                share_receive_date = item['F017D']
                bonus_item = stock_bonusItem(code, notice_date, rightoff_time, stock_right_registe_date, cash_per_share,
        send_bonus_share_per_share, increase_shares_per_share, cash_receive_date, share_receive_date)
                lst_bonus.append(bonus_item)
            stockbaseinfoitme = StockbaseinfoItem()
            stockbaseinfoitme['data_type'] = Const.STOCK_BONUS
            stockbaseinfoitme['data_content'] = lst_bonus
            yield stockbaseinfoitme
        print('-----------end---bonus_parse-----------------------------')

    def info_parse(self,response):
        print('--------------info_parse-----------------------------')
        if len(response.text)>4:
            data = json.loads(response.text)
            dataitem = data[0]
            code=dataitem['5']
            name = dataitem['55']
            price_change = '0.0' if dataitem['264648']=="" else dataitem['264648']
            p_change = '0.0' if dataitem['199112']=="" else dataitem['199112']
            open = '0.0' if dataitem['7']=="" else dataitem['7']
            yesterday_close = '0.0' if dataitem['6']=="" else dataitem['6']
            high = '0.0' if dataitem['8']=="" else dataitem['9']
            low = '0.0' if dataitem['9']=="" else dataitem['9']
            close = '0.0' if dataitem['10']=="" else dataitem['10']
            volume = '0.0' if dataitem['13']=="" else dataitem['13']
            amount = '0.0' if dataitem['19']=="" else dataitem['19']
            stockinfo = stock_infoItem(code, name, open, high, close,
                     low, volume, amount,price_change,
                     p_change, yesterday_close, 0.0, 0.0, 0,
                           0.0, 0.0, time.strftime("%Y-%m-%d", time.localtime(time.time())),0.0)
            stockbaseinfoitme = StockbaseinfoItem()
            stockbaseinfoitme['data_type']=Const.STOCK_INFO
            stockbaseinfoitme['data_content']=stockinfo
            print('-----------end---info_parse-----------------------------')
            yield  stockbaseinfoitme
        # sel = Selector(response)
        # print(response.text)
        #
        # #stock_baseinfo = stock_infoItem()
        # page_stockdetail_sublist = sel.xpath('//div[@class="page-stockdetail"]')
        # code = page_stockdetail_sublist.xpath('//div[@class="sub-code"]/text()').extract_first()
        # name = page_stockdetail_sublist.xpath('//div[@class="sub-title"]/text()').extract_first()
        # close = page_stockdetail_sublist.xpath('//div[@class="sub-trend-value"]/text()').extract_first()
        # price_change = page_stockdetail_sublist.xpath('//div[@class="sub-trend-size"]/text()').extract_first()
        # p_change = page_stockdetail_sublist.xpath('//div[@class="sub-trend-trend"]/text()').extract_first()
        # date = page_stockdetail_sublist.xpath('//div[@class="sub-time last-child"]/text()').extract_first()
        # yesterday_close = page_stockdetail_sublist.xpath('//div[@id="pre"]/text()').extract_first()
        # open = page_stockdetail_sublist.xpath('//div[@id="open"]/text()').extract_first()
        # online_years = page_stockdetail_sublist.xpath('//div[@id="sub-value age"]/text()').extract_first()
        # pb = page_stockdetail_sublist.xpath('//div[@id="pb-ratio"]/text()').extract_first()
        # pe = page_stockdetail_sublist.xpath('//div[@id="pe-ratio"]/text()').extract_first()
        # high = page_stockdetail_sublist.xpath('//div[@id="high"]/text()').extract_first()
        # low  = page_stockdetail_sublist.xpath('//div[@id="low"]/text()').extract_first()
        # volume  = page_stockdetail_sublist.xpath('//div[@id="vol"]/text()').extract_first()
        # amount  = page_stockdetail_sublist.xpath('//div[@id="money"]/text()').extract_first()
        # exchange = page_stockdetail_sublist.xpath('//div[@id="amplit"]/text()').extract_first()
        # turnover = page_stockdetail_sublist.xpath('//div[@id="huanshou"]/text()').extract_first()
        # print(code,name,close,open,price_change,p_change,date,yesterday_close,online_years,pb,pe,high,low,volume,amount,exchange,turnover)
        #
        #
        # StockbaseinfoItem['data_type']= Const.BALANCE_SHEET
        # StockbaseinfoItem['data_type']=""
        #yield StockbaseinfoItem

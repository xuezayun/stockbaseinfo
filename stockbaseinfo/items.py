# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item,Field


class StockbaseinfoItem(scrapy.Item):
    # name = scrapy.Field()
    data_type = Field()
    data_content = Field();
#财务报表
class balance_sheetItem():
    def __init__(self, code, subject_title,account1,account2,account3,account4,account5,account6,account7,account8,account9,account10,
                 year1,year2,year3,year4,year5,year6,year7,year8,year9,year10):
        self.code = code
        self.subject_title = subject_title
        self.account1 = account1
        self.account2 = account2
        self.account3 = account3
        self.account4 = account4
        self.account5 = account5
        self.account6 = account6
        self.account7 = account7
        self.account8 = account8
        self.account9 = account9
        self.account10 = account10
        self.year1 = year1
        self.year2 = year2
        self.year3 = year3
        self.year4 = year4
        self.year5 = year5
        self.year6 = year6
        self.year7 = year7
        self.year8 = year8
        self.year9 = year9
        self.year10 = year10
#现金流量报表
class cash_flowItem():
    def __init__(self, code, subject_title, account1, account2, account3, account4, account5, account6, account7,
                 account8, account9, account10,
                 year1, year2, year3, year4, year5, year6, year7, year8, year9, year10):
        self.code = code
        self.subject_title = subject_title
        self.account1 = account1
        self.account2 = account2
        self.account3 = account3
        self.account4 = account4
        self.account5 = account5
        self.account6 = account6
        self.account7 = account7
        self.account8 = account8
        self.account9 = account9
        self.account10 = account10
        self.year1 = year1
        self.year2 = year2
        self.year3 = year3
        self.year4 = year4
        self.year5 = year5
        self.year6 = year6
        self.year7 = year7
        self.year8 = year8
        self.year9 = year9
        self.year10 = year10
#主要指数
class main_indexItem():
    def __init__(self, code, subject_title,season, account1, account2, account3, account4, account5, account6, account7,
                 account8, account9, account10,
                 year1, year2, year3, year4, year5, year6, year7, year8, year9, year10):
        self.code = code
        self.subject_title = subject_title
        self.season = season
        self.account1 = account1
        self.account2 = account2
        self.account3 = account3
        self.account4 = account4
        self.account5 = account5
        self.account6 = account6
        self.account7 = account7
        self.account8 = account8
        self.account9 = account9
        self.account10 = account10
        self.year1 = year1
        self.year2 = year2
        self.year3 = year3
        self.year4 = year4
        self.year5 = year5
        self.year6 = year6
        self.year7 = year7
        self.year8 = year8
        self.year9 = year9
        self.year10 = year10
#利润表
class profit_sheetItem():
    def __init__(self, code, subject_title,season, account1, account2, account3, account4, account5, account6, account7,
                 account8, account9, account10,
                 year1, year2, year3, year4, year5, year6, year7, year8, year9, year10):
        self.code = code
        self.subject_title = subject_title
        self.season = season
        self.account1 = account1
        self.account2 = account2
        self.account3 = account3
        self.account4 = account4
        self.account5 = account5
        self.account6 = account6
        self.account7 = account7
        self.account8 = account8
        self.account9 = account9
        self.account10 = account10
        self.year1 = year1
        self.year2 = year2
        self.year3 = year3
        self.year4 = year4
        self.year5 = year5
        self.year6 = year6
        self.year7 = year7
        self.year8 = year8
        self.year9 = year9
        self.year10 = year10
#分红
class stock_bonusItem():
    def __init__(self, code, notice_date, rightoff_time, stock_right_registe_date, cash_per_share,
                 send_bonus_share_per_share, increase_shares_per_share, cash_receive_date,share_receive_date):
        self.code = code
        self.notice_date = notice_date
        self.rightoff_time = rightoff_time
        self.stock_right_registe_date = stock_right_registe_date
        self.cash_per_share = cash_per_share
        self.send_bonus_share_per_share = send_bonus_share_per_share
        self.increase_shares_per_share = increase_shares_per_share
        self.cash_receive_date = cash_receive_date
        self.share_receive_date = share_receive_date
#十大流通股东
class stock_holdersItem():
    def __init__(self, code, holder_range, holder_name, stock_count, stock_percent,
                 stock_property,count_date):
        self.code = code
        self.holder_range = holder_range
        self.holder_name = holder_name
        self.stock_count = stock_count
        self.stock_percent = stock_percent
        self.stock_property = stock_property
        self.count_date = count_date
#股票基本信息
class stock_infoItem():
    def __init__(self, code, name, open, high, close,
                 low, volume, amount,price_change,
                 p_change, yesterday_close, exchange,turnover,online_years,
                 pb, pe, date,amplitude):
        self.code = code
        self.name = name
        self.open = open
        self.high = high
        self.close = close
        self.low = low
        self.volume = volume
        self.amount = amount
        self.price_change = price_change
        self.p_change = p_change
        self.yesterday_close = yesterday_close
        self.exchange = exchange
        self.turnover = turnover
        self.online_years = online_years
        self.pb = pb
        self.pe = pe
        self.date = date
        self.amplitude = amplitude

#爬取新浪滚动新闻
class sina_newsItem(scrapy.Item):
    collection = 'newsina'
    ctime = Field()  # 发布时间
    url = Field()
    wapurl = Field()
    title = Field()  # 新闻标题
    media_name = Field()  # 发发布的媒体
    keywords = Field()  #  关键词
    content = Field()  #  新闻内容

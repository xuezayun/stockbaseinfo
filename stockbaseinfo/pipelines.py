# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
# 使用twsited异步IO框架，实现数据的异步写入。
from pymysql import cursors
from twisted.enterprise import adbapi
from stockbaseinfo.settings import *
from stockbaseinfo.Const import *
import traceback

class StockbaseinfoPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        # 从项目的配置文件中读取相应的参数
        cls.MYSQL_DB_NAME = crawler.settings.get("MYSQL_DB_NAME", 'finance_data')
        cls.HOST = crawler.settings.get("MYSQL_HOST", 'localhost')
        cls.PORT = crawler.settings.get("MYSQL_PORT", 3306)
        cls.USER = crawler.settings.get("MYSQL_USER", 'root')
        cls.PASSWD = crawler.settings.get("MYSQL_PASSWORD", 'root')
        return cls()

    def __init__(self):
        dbparams = {
            'host':MYSQL_HOST,
            'port': 3306,
            'user': MYSQL_USER,
            'password': MYSQL_PASSWORD,
            'database': MYSQL_DB_NAME,
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor  # 指定cursor的类
        }
        # 初始化数据库连接池，参数1是mysql的驱动，参数2是连接mysql的配置信息
        self.db_pool = adbapi.ConnectionPool('pymysql', **dbparams)
        # sql语言的空值
        self._sql = None
    def process_item(self, item, spider):
        # 操作数据，将数据写入数据库
        # 如果是同步写入的话，使用的是cursor.execute(),commit()
        # 异步存储的方式：函数方式pool.map(self.insert_db,[1,2])
        query = self.db_pool.runInteraction(self.insert_db, item)
        query.addErrback(self.handle_error, item, spider)

    #依据不同的数据类型进行不同的数据操作
    def insert_db(self, cursor, item):
        data_type = item['data_type']
        if data_type == Const.STOCK_INFO:#股票基本信息
            stockinfo = item['data_content']
            values = (
                stockinfo.code,
                stockinfo.name,
                stockinfo.open,
                stockinfo.high,
                stockinfo.close,
                stockinfo.low,
                stockinfo.code,
                stockinfo.amount,
                stockinfo.price_change,
                stockinfo.p_change,
                stockinfo.yesterday_close,
                stockinfo.exchange,
                stockinfo.online_years,
                stockinfo.pb,
                stockinfo.pe,
                str(stockinfo.date),
                stockinfo.amplitude
            )
            sql = '''INSERT INTO `finance_data`.`stock_basic_info`(`code`,`name`,`open`,`high`,`close`,`low`,`volume`,`amount`,`price_change`,`p_change`,`yesterday_close`,`exchange`,`online_years`,`pb`,`pe`,`date`,`amplitude`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
            try:
                cursor.execute(sql, values)
            except:
                traceback.print_exc()
        elif data_type == Const.BALANCE_SHEET: #资产负债表
            lstblancesheet =  item['data_content']
            for blancesheet in lstblancesheet:
                values = (
                    blancesheet.code,
                    blancesheet.subject_title,
                    blancesheet.account1,
                    blancesheet.account2,
                    blancesheet.account3,
                    blancesheet.account4,
                    blancesheet.account5,
                    blancesheet.account6,
                    blancesheet.account7,
                    blancesheet.account8,
                    blancesheet.account9,
                    blancesheet.account10,
                    blancesheet.year1,
                    blancesheet.year2,
                    blancesheet.year3,
                    blancesheet.year4,
                    blancesheet.year5,
                    blancesheet.year6,
                    blancesheet.year7,
                    blancesheet.year8,
                    blancesheet.year9,
                    blancesheet.year10
                )
                sql = '''INSERT INTO `finance_data`.`stock_basic_balance_sheet`(`code`,`subject_title`,`account1`,`account2`,`account3`,`account4`,`account5`,`account6`,`account7`,`account8`,`account9`,
                `account10`,`year1`,`year2`,`year3`,`year4`,`year5`,`year6`,`year7`,`year8`,`year9`,`year10`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
                try:
                    cursor.execute(sql, values)
                except:
                    traceback.print_exc()
        elif data_type == Const.CASH_FLOW: #资产负债表
            lstbcashflow =  item['data_content']
            for cashflow in lstbcashflow:
                values = (
                    cashflow.code,
                    cashflow.subject_title,
                    cashflow.account1,
                    cashflow.account2,
                    cashflow.account3,
                    cashflow.account4,
                    cashflow.account5,
                    cashflow.account6,
                    cashflow.account7,
                    cashflow.account8,
                    cashflow.account9,
                    cashflow.account10,
                    cashflow.year1,
                    cashflow.year2,
                    cashflow.year3,
                    cashflow.year4,
                    cashflow.year5,
                    cashflow.year6,
                    cashflow.year7,
                    cashflow.year8,
                    cashflow.year9,
                    cashflow.year10
                )
                sql = '''INSERT INTO `finance_data`.`stock_basic_cashflow_sheet`(`code`,`subject_title`,`account1`,`account2`,`account3`,`account4`,`account5`,`account6`,`account7`,`account8`,`account9`,
                `account10`,`year1`,`year2`,`year3`,`year4`,`year5`,`year6`,`year7`,`year8`,`year9`,`year10`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
                try:
                    cursor.execute(sql, values)
                except:
                    traceback.print_exc()
        elif data_type == Const.PROFIT_SHEET:  # 利润表
            lstprofit = item['data_content']
            for profit in lstprofit:
                values = (
                    profit.code,
                    profit.subject_title,
                    profit.season,
                    profit.account1,
                    profit.account2,
                    profit.account3,
                    profit.account4,
                    profit.account5,
                    profit.account6,
                    profit.account7,
                    profit.account8,
                    profit.account9,
                    profit.account10,
                    profit.year1,
                    profit.year2,
                    profit.year3,
                    profit.year4,
                    profit.year5,
                    profit.year6,
                    profit.year7,
                    profit.year8,
                    profit.year9,
                    profit.year10
                )
                sql = '''INSERT INTO `finance_data`.`stock_basic_profit_sheet`(`code`,`subject_title`,`season`,`account1`,`account2`,`account3`,`account4`,`account5`,`account6`,`account7`,`account8`,`account9`,
                 `account10`,`year1`,`year2`,`year3`,`year4`,`year5`,`year6`,`year7`,`year8`,`year9`,`year10`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
                try:
                    cursor.execute(sql, values)
                except:
                    traceback.print_exc()
        elif data_type == Const.STOCK_BONUS:  # 历史分红表
            lstbonus = item['data_content']
            for bonus in lstbonus:
                values = (
                    bonus.code,
                    bonus.notice_date,
                    bonus.rightoff_time,
                    bonus.stock_right_registe_date,
                    bonus.cash_per_share,
                    bonus.send_bonus_share_per_share,
                    bonus.increase_shares_per_share,
                    bonus.cash_receive_date,
                    bonus.share_receive_date
                )
                sql = '''INSERT INTO `finance_data`.`stock_basic_bonus`(`code`,`notice_date`,`rightoff_time`,`stock_right_registe_date`,`cash_per_share`,`send_bonus_share_per_share`,`increase_shares_per_share`,`cash_receive_date`,`share_receive_date`)
VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
                try:
                    cursor.execute(sql, values)
                except:
                    traceback.print_exc()
        elif data_type == Const.MAIN_INDEX:  # 历史分红表
            lstmainindex = item['data_content']
            for mainindex in lstmainindex:
                values = (
                    mainindex.code,
                    mainindex.subject_title,
                    mainindex.season,
                    mainindex.account1,
                    mainindex.account2,
                    mainindex.account3,
                    mainindex.account4,
                    mainindex.account5,
                    mainindex.account6,
                    mainindex.account7,
                    mainindex.account8,
                    mainindex.account9,
                    mainindex.account10,
                    mainindex.year1,
                    mainindex.year2,
                    mainindex.year3,
                    mainindex.year4,
                    mainindex.year5,
                    mainindex.year6,
                    mainindex.year7,
                    mainindex.year8,
                    mainindex.year9,
                    mainindex.year10
                )
                sql = '''INSERT INTO `finance_data`.`stock_basic_main_index`(`code`,`subject_title`,`season`,`account1`,`account2`,`account3`,`account4`,`account5`,`account6`,`account7`,`account8`,`account9`,
                 `account10`,`year1`,`year2`,`year3`,`year4`,`year5`,`year6`,`year7`,`year8`,`year9`,`year10`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
                try:
                    cursor.execute(sql, values)
                except:
                    traceback.print_exc()
        elif data_type == Const.STOCK_HOLDERS:  # 前十大股东表
            lststockholders = item['data_content']
            for stockholder in lststockholders:
                values = (
                    stockholder.code,
                    stockholder.holder_range,
                    stockholder.holder_name,
                    stockholder.stock_count,
                    stockholder.stock_percent,
                    stockholder.stock_property,
                    stockholder.count_date
                )
                sql = '''INSERT INTO `finance_data`.`stock_basic_holders`(`code`,`holder_range`,`holder_name`,`stock_count`,`stock_percent`,`stock_property`,`count_date`)VALUES(%s,%s,%s,%s,%s,%s,%s);'''
                try:
                    cursor.execute(sql, values)
                except:
                    traceback.print_exc()
        elif data_type == Const.ROLL_NEWS:  # 获取所有新闻信息
            lstnews = item['data_content']
            for newitem in lstnews:
                values = (
                    newitem['title'],
                    newitem['content'],
                    newitem['ctime'],
                    newitem['media_name'],
                    newitem['keywords'],
                    newitem['url'],
                    newitem['wapurl']
                )
                sql = '''INSERT INTO `finance_basic_data`.`sina_news`(`title`,`content`,`ctime`,`media_name`,`keywords`,`url`,`wepurl`)VALUES(%s,%s,%s,%s,%s,%s,%s);'''
                try:
                    cursor.execute(sql, values)
                except:
                    traceback.print_exc()

    def handle_error(self, error, item, spider):
        print('=' * 10 + "error" + '=' * 10)

# -*- coding:utf-8 - *-

import datetime,time
import db_tools as dt
import math
from stockbaseinfo.Const import *
import requests

class Utils(object):

    #获取某daysago天数之前的日期
    @staticmethod
    def get_num_startdate(daysnum = 1):
        lstretdate =[]
        selectdaysago ='''select date from hist_data where code = '000001' order by date desc limit %d;'''%daysnum
        lstitem = Utils.fetch_data(selectdaysago)
        for item in lstitem:
            date = item[0]
            lstretdate.append(date.strftime('%Y-%m-%d'))
        return lstretdate;

    # 获取某daysnum天数之前的日期
    @staticmethod
    def get_fourdate(daysnum=4):
        selectdaysago = '''select date from hist_data where code = '000001' order by date desc limit %d;''' % daysnum
        lstitem = Utils.fetch_data(selectdaysago)
        day3date = lstitem[3][0]
        day2date = lstitem[2][0]
        day1date = lstitem[1][0]
        daydate = lstitem[0][0]
        day3Date = day3date.strftime('%Y-%m-%d')
        day2Date = day2date.strftime('%Y-%m-%d')
        day1Date = day1date.strftime('%Y-%m-%d')
        dayDate = daydate.strftime('%Y-%m-%d')
        return day3Date,day2Date,day1Date,dayDate;
    @staticmethod
    def get_lastdate():
        selectdaysago = '''select date from hist_data where code = '000001' order by date desc limit 1;'''
        lstitem = Utils.fetch_data(selectdaysago)
        if len(lstitem)>0 :
            startdate = lstitem[0][0]
        return startdate.strftime('%Y-%m-%d')
    # 执行SQL语句集合
    @staticmethod
    def execute_data(lstinsertsql):
        dbTools = dt.DbTools()
        dbTools.connect()
        dbTools.insertorupdate_data(lstinsertsql)
        dbTools.commit_data()

    # 获取查询数据
    @staticmethod
    def fetch_data(querysql):
        dbTools = dt.DbTools()
        dbTools.connect()
        lstitem = dbTools.fetch_data(querysql)
        for item in lstitem:
            temsql = ''
            for i in range(len(item)):
                temsql += '\'' + str(item[i]) + '\','
        dbTools.close()
        return lstitem;

    @staticmethod
    def time_cmp(first_time,second_time):
        return int(time.strftime("%H%M%S", time.strptime(str(first_time), "%H:%M:%S"))) < int(time.strftime("%H%M%S", second_time))






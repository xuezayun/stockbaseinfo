# -*- coding:utf-8 -*-
import pymysql
import sys
from stockbaseinfo.Const import *

#调用方法
# dbTools = new DbTools()

class DbTools:
    conn = None
    cursor = None
    #建立和数据库系统得连接
    def connect(self):
        self.conn = pymysql.connect(host=Const.DB_SERVER,port=Const.PORT,user=Const.DB_USER, passwd=Const.DB_PWD,db=Const.DB_NAME,charset="utf8")
        self.cursor = self.conn.cursor();

    def insertorupdate_data(self,lstsql):
        try:
            for sql in lstsql:
                self.cursor.execute(sql)
        except:
            print("except")
        finally:
            print("finally")


    def fetch_data(self,sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def commit_data(self):
        self.cursor.close()
        self.conn.commit()
        return self.conn.close()

    def close(self):
        self.cursor.close()
        return self.conn.close()




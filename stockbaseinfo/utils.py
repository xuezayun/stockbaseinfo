# -*- coding:utf-8 - *-

class Utils(object):
    #计算有效的时间和数据
    @staticmethod
    def load_validdata(lstyear,item):
        lstyear.sort(reverse=True)
        arr_year = ["1900" for _ in range(10)]
        arr_item = ['0' for _ in range(10)]
        for i in range(len(lstyear)):
            arr_year[9 - i] = lstyear[i]
            arr_item[9 - i] = item[lstyear[i]]
        return arr_year, arr_item
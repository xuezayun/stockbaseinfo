# -*- coding: utf-8 -*-
from scrapy import Request
from ..items import *
from ..Const import *
import random
import json
import re
from datetime import datetime


class newsSpider(scrapy.Spider):
    name = "news"
    lstsinanews = []
    base_url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid={}&k=&num=50&page={}&r={}'
    #     "2509": "全部",
    #     "2510": "国内",
    #     "2511": "国际",
    #     "2669": "社会",
    #     "2512": "体育",
    #     "2513": "娱乐",
    #     "2514": "军事",
    #     "2515": "科技",
    #     "2516": "财经",
    #     "2517": "股市",
    #     "2518": "美股",
    #     "2968": "国内_国际",
    #     "2970": "国内_社会",
    #     "2972": "国际_社会",
    #     "2974": "国内国际社会"
    def start_requests(self):
        #  可修改  这里设置爬取100页
        self.page_total = 24
        # self.page_total = 1
        for page in range(1, self.page_total + 1):
            #  按上面注释  可修改 这里"2509"代表"全部"类别的新闻
            lid = "2516"
            r = random.random()
            yield Request(self.base_url.format(lid, page, r), callback=lambda response,page=page:self.parse(response,page))

    def parse(self, response,page):
        result = json.loads(response.text)
        data_list = result.get('result').get('data')
        icount = 0
        totalcount = len(data_list)
        print("totalcount:"+str(totalcount))
        for data in data_list:
            icount += 1
            item = sina_newsItem()
            ctime = datetime.fromtimestamp(int(data.get('ctime')))
            ctime = datetime.strftime(ctime, '%Y-%m-%d %H:%M')
            item['ctime'] = ctime
            item['url'] = str(data.get('url')).strip()
            item['wapurl'] = str(data.get('wapurl')).strip()
            item['title'] = str(data.get('title')).strip()
            item['media_name'] = str(data.get('media_name')).strip()
            item['keywords'] = str(data.get('keywords')).strip()
            yield Request(url=item['url'], callback=lambda response,page=page,isend = icount == totalcount:self.parse_content(response,page,isend) , meta={'item': item})

        # 进入到详情页面 爬取新闻内容

    def parse_content(self, response,page,isend):
        item = response.meta['item']
        content = ''.join(response.xpath('//*[@id="artibody" or @id="article"]//p/text()').extract())
        content = re.sub(r'\u3000', '', content)
        content = re.sub(r'[ \xa0?]+', ' ', content)
        content = re.sub(r'\s*\n\s*', '\n', content)
        content = re.sub(r'\s*(\s)', r'\1', content)
        content = ''.join([x.strip() for x in content])
        # content_list = response.xpath('//*[@id="artibody" or @id="article"]//p/text()').extract()
        # content = r""
        # for part in content_list:
        #     part = part.strip()
        #     content += part
        item['content'] = content
        print("page:"+str(page)+",isend:"+str(isend))
        if self.page_total == page and isend:
            stockbaseinfoitme = StockbaseinfoItem()
            stockbaseinfoitme['data_type'] = Const.ROLL_NEWS
            stockbaseinfoitme['data_content'] = self.lstsinanews
            yield stockbaseinfoitme
        else:
            self.lstsinanews.append(item)


# -*- coding: utf-8 -*-
import scrapy
import jsonpath
import json
from  ..items import FenbiItem

class FenbiSpider(scrapy.Spider):
    name = "fenbi"
    allowed_domains = ['fenbi.com']

    #重写Spider类中的start_requests，生成自定义的request对象，因为默认request对象,可能并不包含你需要的内容，比如你想设置cookie，meta，数据等
    def start_requests(self):
        urls = [
            'https://fenbi.com/web/users/course/gwy?kav=12&start=1'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        li = json.loads(response.text).get('courseInfo')
        for item in li:
            for key, val in item.items():
                if isinstance(val,dict):
                    if 'bestDiscount' in val:
                        val.pop('bestDiscount')
                    if 'discounts' in val:
                        val.pop('discounts')
        #print(jsonpath.jsonpath(li,'$..title'),jsonpath.jsonpath(json.loads(response.text),'$..totalPages')[0])
        items = FenbiItem()
        items['book_title'] = jsonpath.jsonpath(li,'$..title')
        print(items)
        #print(jsonpath.jsonpath(json.loads(response.text),'$.courseInfo[?(@.apeCourseId)]'))
        #print(jsonpath.jsonpath(json.loads(response.text).get('courseInfo'),'$..id'))
        #print(json.loads(response.text).get('courseInfo'))
        #print(json.loads(response.text).get('courseInfo"'))
        current_page = jsonpath.jsonpath(json.loads(response.text),'$..currentPage')[0]
        total_pages = jsonpath.jsonpath(json.loads(response.text),'$..totalPages')[0]
        if current_page <= total_pages-1:
            next_page = "https://fenbi.com/web/users/course/gwy?kav=12&start=%d"%(current_page+1)
            yield scrapy.Request(next_page, callback=self.parse)
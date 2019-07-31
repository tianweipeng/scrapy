# -*- coding: utf-8 -*-
import scrapy
import jsonpath
import json
from  ..items import FenbiItem

class FenbiSpider(scrapy.Spider):
    name = "fenbi"
    allowed_domains = ['www.fenibi.com']

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
        i = 2
        while i <= jsonpath.jsonpath(json.loads(response.text),'$..totalPages')[0]:
            url = "https://fenbi.com/web/users/course/gwy?kav=12&start=%d"%i
            i+=1
            print(i)
            print(url)
            yield scrapy.Request(url=url, callback=self.parse)

# class QuotesSpider(scrapy.Spider):
#     name = "quotes"
#     urls = [
#         'http://quotes.toscrape.com/page/1/',
#         'http://quotes.toscrape.com/page/2/',
#     ]
#
#     def parse(self, response):
#         page = response.url.split("/")[-2]
#         filename = 'quotes-%s.html' % page
#         with open(filename, 'wb') as f:
#             f.write(response.body)
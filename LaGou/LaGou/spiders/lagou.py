# -*- coding: utf-8 -*-
import scrapy
import json


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['lagou.com']
    def start_requests(self):
        urls = [
            'https://www.lagou.com'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

#请求头中的Referer必须是https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=，所以再转跳一次，将Referer置为该url，否则显示请求太频繁
    def parse(self, response):
        yield scrapy.Request(
            url='https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
            callback=self.zhuantiao
        )

    def zhuantiao(self, response):
        data = {
            'first': 'True',
            'pn': '1',
            'kd': 'python'
        }
        yield scrapy.FormRequest(
            url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false',
            formdata = data,
            callback = self.afterlogin

            #headers = response.headers
        )
    def afterlogin(self, response):
        print(json.loads(response.text))

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
    def parse(self, response):
        #print(response.xpath('//*[@id="lg_tbar"]/div/ul/li[5]/a/text()').extract())
        #Cookie1 = response.headers.getlist('Set-Cookie')
        #print('后台首次写入的响应Cookies：',Cookie1)
        data = {
            'first': 'true',
            'pn': '1',
            'kd': 'python'
        }
        yield scrapy.FormRequest(
            url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false',
            cookies = response.cookie,
            formdata = data,
            callback = self.afterlogin
        )
    def afterlogin(self, response):
        print(json.loads(response.text))

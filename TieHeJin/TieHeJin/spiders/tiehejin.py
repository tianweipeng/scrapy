# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class TiehejinSpider(scrapy.Spider):
    name = 'tiehejin'
    allowed_domains = ['cnfeol.com']
    url = 'http://www.cnfeol.com/'
    lua_scripts ="""
                function main(splash, args)
                  assert(splash:go(args.url))
                  assert(splash:wait(args.wait))
                  user_text = splash:select("#Signin_MemberName")
                  pass_text = splash:select("#Signin_MemberPassword")
                  login_btn = splash:select("#Signin_Submit")
                  user_text:send_text("18648258827")
                  pass_text:send_text("41458woaixinxin")
                  login_btn:mouse_click({})
                  splash:wait(10)
                  return {
                    html = splash:html()
                     }
            end
    """

    def start_requests(self):
        yield SplashRequest(self.url, callback=self.parse, endpoint='execute',
                            args={'lua_source': self.lua_scripts,'wait': 5})

    def parse(self, response):
        with open('thj.html','w',encoding='utf-8') as f:
            f.write(response.text)

# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
import time

class SeleniumMiddleware(object):
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        # 设置窗口大小以
        self.chrome_options.add_argument('--window-size=1366,768')
        # 设置浏览器窗口无痕模式
        # self.chrome_options.add_argument('--incognito')
        # 取消显示“浏览器正在受到自动软件的控制”
        self.chrome_options.add_argument('--disable-infobars')
        # 启动浏览器
        self.browser = webdriver.Chrome(chrome_options=self.chrome_options)
    def process_request(self, request, spider):
        if request.url == 'https://www.lagou.com':
            self.browser.get(request.url)
            self.browser.find_element_by_xpath('//*[@id="cboxClose"]').click()
            time.sleep(1)
            self.browser.find_element_by_xpath('//*[@id="lg_tbar"]/div/div[2]/div/a[1]').click()
            self.browser.find_element_by_xpath("/html/body/div[2]/div[1]/div/div/div[2]/div[3]/div[1]/div/div[1]/form/div[1]/input").send_keys('18648258827')
            time.sleep(2)
            self.browser.find_element_by_xpath(
                "/html/body/div[2]/div[1]/div/div/div[2]/div[3]/div[1]/div/div[1]/form/div[2]/input").send_keys(
                '41458woaixinxin')
            self.browser.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/div[2]/div[3]/div[2]/div[2]/div[2]').click()
            time.sleep(20)
            cookies = {}
            seleniumCookies = self.browser.get_cookies()
            for cookie in seleniumCookies:
                for key, val in cookie.items():
                    if key == 'name':
                        cookies[cookie[key]] = cookie['value']
            request.cookies = cookies
            #print(f"seleniumCookies = {cookies}")

    def process_response(self, request, response, spider):
        cookie = request.cookies
        response.cookie = cookie
        print(cookie)
        return response



class LagouSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class LagouDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

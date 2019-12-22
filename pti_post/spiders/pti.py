# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.selector import Selector


class PtiSpider(scrapy.Spider):
    name = 'pti'
    allowed_domains = ['www.ptinews.com']
    i = 2
    payload = """
    {"pnum":1,"txtser":"","selcat":"select"}
    """
    def start_requests(self):
        yield scrapy.Request(url='http://www.ptinews.com/pressrelease/pressrelease.aspx/changePreData', 
              method='POST',
              body=self.payload, 
              headers={
             'Content-Type': "application/json; charset=UTF-8",
             'Cookie': "undefined=undefined; ASP.NET_SessionId=eqkjoy2rjkbey555devbqcus",
             'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
             })

    def parse(self, response):
        data = json.loads(response.text)
        if data != "none":
            selector = scrapy.Selector(text=data, type="html")
            row = selector.xpath('//table/tr/td/table/tr')
            for each in row:
                yield {
                    'News Title':each.xpath('.//td[1]/a/text()').get(),
                    'Source': each.xpath('.//td[3]/text()').get(),
                    'Category':each.xpath('.//td[5]/text()').get(),
                    'Date':each.xpath('.//td[7]/text()').get(),
                }
            new_payload = """
            {"pnum":1,"txtser":"","selcat":"select"}
            """
            new_payload = json.loads(new_payload)
            new_payload['pnum'] = self.i
            self.i += 1
            yield scrapy.Request(url='http://www.ptinews.com/pressrelease/pressrelease.aspx/changePreData', 
            method='POST',
            body=json.dumps(new_payload), 
            headers={
            'Content-Type': "application/json; charset=UTF-8",
            'Cookie': "undefined=undefined; ASP.NET_SessionId=eqkjoy2rjkbey555devbqcus",
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            })
        else:
            print("Page not exist",self.i)

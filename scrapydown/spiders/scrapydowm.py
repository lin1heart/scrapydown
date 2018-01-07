# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapydown.items import ScrapydownItem

class ScrapydowmSpider(scrapy.Spider):
    name = 'scrapydowm'
    allowed_domains = ["meizitu.com"]

    start_urls = [
        'http://www.meizitu.com/a/5402.html',
        'http://www.meizitu.com/a/5381.html'
    ]

    def parse(self, response):
        sel = Selector(response)
        image_url = sel.xpath('//*[@id="picture"]/p/img/@src').extract()
        print('the urls:/n')
        print(image_url)
        print('/n')

        item = ScrapydownItem()
        item['url'] = image_url

        yield item

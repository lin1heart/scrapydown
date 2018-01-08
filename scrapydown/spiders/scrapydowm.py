# -*- coding: utf-8 -*-
import scrapy
import string
from scrapy.selector import Selector
from scrapydown.items import ScrapydownItem
title = ''
class ScrapydowmSpider(scrapy.Spider):
    name = 'scrapydowm'
    allowed_domains = ["meizitu.com"]

    start_urls = [
        'http://www.meizitu.com/a/more_1.html'
        # 'http://www.meizitu.com/a/5381.html'
    ]
    # wait_url = 'http://www.meizitu.com/a/'
    detil_title = []


    def parse(self, response):
        global detil_title
        global title
        sear = Selector(response)
        total_ui = sear.xpath('//ul[@class="wp-list clearfix"]')
        for each in total_ui:
            detil_url = each.xpath('//li/div/h3/a/@href').extract()
            detil_title = each.xpath('//li/div/h3/a/b/text()').extract()
        for a in detil_url:
            yield scrapy.http.Request(a, callback=self.detil)
            
        next_url = sear.xpath('//*[@id="wp_page_numbers"]/ul/li')[-2].xpath('a/@href').extract()
        if next_url:
            next = next_url[0]
            print next
            yield scrapy.http.Request('http://www.meizitu.com/a/' + next, callback=self.parse)

    def detil(self, response):
#        global title
        sel = Selector(response)
        image_url = sel.xpath('//*[@id="picture"]/p/img/@src').extract()
        title = sel.xpath('//*[@id="picture"]/p/img/@alt')[0].extract()
        if len(title) ==0:
            title = 'error'
        else:
            title = title.split(u'第')[0].replace(u'，', '')
        url_title = []
        for each in image_url:
            url_title.append(each + title)
        item = ScrapydownItem()
        item['url'] = image_url
        item['title'] = url_title
        yield item
        
    def is_chinese(self, uchar):
#    """判断一个unicode是否是汉字"""
        if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
            return True
        else:
            return False
        
    def format_str(self, content):
        content_str = ''
        for i in content:
            if self.is_chinese(i):
                content_str = content_str+i
        return content_str

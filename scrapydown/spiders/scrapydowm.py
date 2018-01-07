# -*- coding: utf-8 -*-
import scrapy
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
        sear = Selector(response)
        total_ui = sear.xpath('//ul[@class="wp-list clearfix"]')
        # print total_ui
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
        global title
        sel = Selector(response)
        image_url = sel.xpath('//*[@id="picture"]/p/img/@src').extract()
        title = sel.xpath('//*[@id="picture"]/p/img/@alt')[0].extract()
        item = ScrapydownItem()
        item['url'] = image_url
        item['title'] = detil_title
        print 'title is ', title
        yield item

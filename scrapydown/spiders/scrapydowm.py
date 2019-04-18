# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapydown.items import ScrapydownItem
title = ''
class ScrapydowmSpider(scrapy.Spider):
    name = 'scrapydowm'
    allowed_domains = ["win4000.com"]

    start_urls = [
        'http://www.win4000.com/meinvtag14366_1.html'
        # 'http://www.meizitu.com/a/5381.html'
    ]
    # wait_url = 'http://www.meizitu.com/a/'
    detil_title = []


    def parse(self, response):
        global detil_title
        global title
        sear = Selector(response)
        total_ui = sear.xpath('//div[@class="Left_bar"]')
        for each in total_ui:
            detil_url = each.xpath('//div[@class="list_cont Left_list_cont  Left_list_cont2"]/div[@class="tab_tj"]/div/div/ul/li/a/@href').extract()
            detil_title = each.xpath('//div[@class="list_cont Left_list_cont  Left_list_cont2"]/div[@class="tab_tj"]/div/div/ul/li/a/p/text()').extract()
        print detil_title
        for a in detil_url:
            yield scrapy.http.Request(a, callback=self.detil)
            
        next_url = sear.xpath('//div[@class="pages"]/div/a[@class="next"]/@href').extract()
        if next_url:
            next = next_url[0]
            print next
            yield scrapy.http.Request(next, callback=self.parse)

    def detil(self, response):
        sel = Selector(response)
        image_url = sel.xpath('//div[@class="pic-next-img"]/a/@href')[0].extract()
        print image_url
#        title = sel.xpath('//*[@class="ptitle"]/h1/test()')[0].extract()
        number = sel.xpath('//div[@class="ptitle"]/em/text()')[0].extract()
        number = int(number) +1;
        print number
        for nub in range(1,number):
            nub_url = image_url.split('_')[0] + "_" + str(nub) + ".html"
            nub_url = str(nub_url)
            print nub_url
            yield scrapy.http.Request(nub_url, callback=self.detilImg)

#        else:
#            title = title.split(u'第')[0].replace(u'，', '')
        
        
    def detilImg(self,response):
        sel = Selector(response)
        image_url = sel.xpath('//div[@class="main-wrap"]/div[@id="pic-meinv"]/a/img/@url').extract()
        title = sel.xpath('//div[@class="ptitle"]/h1/text()')[0].extract()
        if len(title) ==0:
            title = 'error'
        url_title = []
        for each in image_url:
            url_title.append(each + title)
        item = ScrapydownItem()
        item['url'] = image_url
        item['title'] = url_title
        yield item
#        
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

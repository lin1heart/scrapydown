# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import re

class IpProxySpider(scrapy.Spider):
    name = 'ip_proxy'
    allowed_domains = ['xicidaili.com/nt/1']
    start_urls = ['http://xicidaili.com/nt/1/']

    def parse(self, response):
        sear = Selector(response)
        print sear
        res_tr = r'<tr>(.*?)</tr>'
        m_tr =  re.findall(res_tr,sear,re.S|re.M) 
        print m_tr

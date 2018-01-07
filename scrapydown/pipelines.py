# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
import scrapydown.spiders.scrapydowm

class ScrapydownPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('uploads')[-1].replace('/', '')
        aa = scrapydown.spiders.scrapydowm.title.split(u'第')[0].replace(u'，', '')
        print aa
        return aa+'/%s' % (image_guid)

    def get_media_requests(self, item, info):
        for image_url in item['url']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        # print 'item is !!!!!', item
        # print 'results is !!!!!', results
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('图片未下载好 %s'%image_paths)
        return item

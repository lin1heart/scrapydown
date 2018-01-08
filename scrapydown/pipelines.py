# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import scrapydown.spiders.scrapydowm

class ScrapydownPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['url']:
            yield Request(url=image_url, meta={'item': item, 'img_url':image_url})
    
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        url = request.meta['img_url']
        aa = item['title']
        name = ''
        for check in aa:
            if check.find(url) !=-1:
                name = check.replace(url, '')
                break
            else:
                name = 'error'
        name = self.format_str(name)
#        print 'name is ', name
        image_guid = request.url.split('uploads')[-1].replace('/', '')
        print image_guid
        return name+'/%s' % (image_guid)
    
    def item_completed(self, results, item, info):
        # print 'item is !!!!!', item
        # print 'results is !!!!!', results
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('图片未下载好 %s'%image_paths)
        return item

    def is_chinese(self, uchar):
#    """判断一个unicode是否是汉字"""
        if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
            return True
        else:
            return False
        
    def format_str(self, content):
        if content == 'error':
            return 'error'
        else:
            content_str = ''
            for i in content:
                if self.is_chinese(i):
                    content_str = content_str+i
            return content_str
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
import logging
import MySQLdb
import MySQLdb.cursors
from PIL import Image
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
from PIL import ImageFile
from twisted.enterprise import adbapi
from settings import IMAGES_STORE

ImageFile.LOAD_TRUNCATED_IMAGES = True

logging.warning("This is a warning")
logging.log(logging.WARNING, "This is a warning")
# 获取实例对象
logger = logging.getLogger()
logger.warning("这是警告消息")
# 指定消息发出者
logger = logging.getLogger('SimilarFace')
logger.warning("This is a warning")


class DuplicatesPipeline(object):

    def __init__(self):
        self.url_seen = set()

    def process_item(self, item, spider):
        for url in item['url']:
            if url in self.url_seen:  # 这里替换成你的item['#']
                raise DropItem("Duplicate item found: %s" % item)
                print '已存在！！！', url
            else:
                self.url_seen.add(url)  # 这里替换成你的item['#']
        return item

class ScrapydownPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['url']:
            yield Request(url=image_url, meta={'item': item, 'img_url': image_url})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        url = request.meta['img_url']
        aa = item['title']
        name = ''
        for check in aa:
            if check.find(url) != -1:
                name = check.replace(url, '')
                break
            else:
                name = 'error'
        name = self.format_str(name)
        if name == '':
            name = 'error'
        image_guid = request.url.split('uploads')[-1].replace('/', '')
        logger.info('name is %s', image_guid)
        logger.info('path is %s', name)
        return name + '/%s' % image_guid

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('图片未下载好 %s' % image_paths)
        item['images'] = image_paths
        return item

    @staticmethod
    def is_chinese(uchar):
        if u'\u4e00' <= uchar <= u'\u9fa5':
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
                    content_str = content_str + i
            return content_str


class MySQLPipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    # pipeline默认调用
    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._conditional_insert, item)
        return d

    @staticmethod
    def _conditional_insert(tb, item):
        ti = round(time.time() * 1000)
        img0 = Image.open(IMAGES_STORE + item['images'][0])
        title0 = item['images'][0].split('/')[0]
        size0 = img0.size
        tb.execute('insert into image_list (id, head_image, height, title, type, upload_dt, width) '
                   'values (%s, %s, %s, %s, %s, %s, %s)',
                   (ti, '3/' + item['images'][0], size0[1], title0, '3', ti, size0[0]))
        for a in item["images"]:
            img = Image.open(IMAGES_STORE + a)
            size = img.size
            tb.execute('insert into image_detail (width, height, image_list_id, url) values (%s, %s, %s, %s)',
                       (size[0], size[1], ti, '3/' + a))

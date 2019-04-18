# scrapydown

一个基于python2.7 + scrapy 框架的爬虫练手项目，爬取的是[美卓](http://www.win4000.com/meinvtag14366_1.html)网站(随手找的一个网站)中的萌宠图片。
获取的图片展示在[gallery](https://fe2o3.club/gallery/)上(自己写的一个Vue项目)

## Init
  因为scrapy框架缘故，只能用python2.7的版本，使用python3.0+会有问题。
  使用pip安装scrapy
  
## Configuration
settings.py文件中：

    MYSQL_HOST = 'localhost'
    MYSQL_DBNAME = 'page'
    MYSQL_USER = 'root'
    MYSQL_PASSWD = 'root'
    IMAGES_STORE = '../dbImage/2/'
前4个全是数据库的配置，最后是图片保存路径，这里我用的是相对路径。

middlewares.py文件中：

    import random
    from settings import USER_AGENT

    # 随机使用预定义列表里的 User-Agent类
    class RandomUserAgent(object):
        def __init__(self, agents):
            # 使用初始化的agents列表
            self.agents = agents

        @classmethod
        def from_crawler(cls, crawler):
            # 获取settings的USER_AGENT列表并返回
            return cls(crawler.settings.getlist('USER_AGENTS'))

        def process_request(self, request, spider):
            # 随机设置Request报头header的User-Agent
            new_user = random.choice(USER_AGENT)
            print '*****USER_AGENT*****', new_user
            request.headers.setdefault('User-Agent', new_user)
USER_AGENT是settings.py文件中定义好的请求头部的User-Agent

## Run
根目录下运行run.py文件
    python run.py

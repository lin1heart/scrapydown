# scrapydown

一个基于python2.7 + scrapy 框架的爬虫练手项目，爬取的是[美桌](http://www.win4000.com/meinvtag14366_1.html)网站(随手找的一个网站)中的萌宠图片，下载图片的同时把图片路径保存在mysql数据库里，用于网站上展示方便。
获取的图片展示在[gallery](https://gallery.util.online/)上(自己写的一个Vue项目)

[个人博客](https://lin1heart.cn/#/post/14)介绍

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

## Run
根目录下运行run.py文件

    python run.py

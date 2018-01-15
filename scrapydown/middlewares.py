# -*- coding: UTF-8 -*-
import random
import base64
# 导入settings的PROXIES设置
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

class IngoreRequestMiddleware(object):  
    def __init__(self):  
        self.middlewareLogging=getLogger("IngoreRequestMiddleware")  
  
    def process_request(self,request,spider):  
        if get_redis_values_1(request.url):  
            self.middlewareLogging.debug("IgnoreRequest : %s" % request.url)  
            raise IgnoreRequest("IgnoreRequest : %s" % request.url)  
        else:  
            self.middlewareLogging.debug("haveRequest : %s" % request.url)  
            return None  

# -*- coding: UTF-8 -*-
import random
import base64
# 导入settings的PROXIES设置
from settings import PROXIES
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
        print '**', request.url
        print '*****USER_AGENT*****', new_user
        request.headers.setdefault('User-Agent', new_user)

# 随机使用预定义列表里的 Proxy代理
class ProxyMiddleware(object):
    # 初始化
    def __init__(self, ip=''):
        self.ip = ip
        
        # 请求处理
        def process_request(self, request, spider):
            # 先随机选择一个IP
            this_ip = random.choice(PROXIES)
            print("当前使用IP是："+ this_ip["ip_port"])
            request.meta["proxy"] = "http://"+thisip["ip_port"]
#        def process_request(self, request, spider):
#            # 随机获取from settings import PROXIES里的代理
#            proxy = random.choice(PROXIES)
#            print request.headers
#            # 如果代理可用，则使用代理
#            if proxy['user_pass'] is not None:
#                request.meta['proxy'] = "http://%s" + proxy['ip_port']
#                print '*****代理*****', proxy['ip_port']
#                # 对代理数据进行base64编码
#                encoded_user_pass = base64.encodestring(proxy['user_pass'])
#                # 添加到HTTP代理格式里
#                request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
#            else:
#                print "****代理失效****" + proxy['ip_port']
#                request.meta['proxy'] = "http://%s" % proxy['ip_port']

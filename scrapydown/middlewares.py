# -*- coding: UTF-8 -*-
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

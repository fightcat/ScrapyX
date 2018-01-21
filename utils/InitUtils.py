# coding:utf-8
"""
初始化，清空所有数据，重新开始新一轮任务
"""
from MongoUtils import MongoUtils
import os
from configs.Settings import *
import configs.Settings

class InitUtils:
    def __init__(self):
        self.mongoUtils = MongoUtils()
        pass

    def init(self):
        db = Settings.MONGO_DB
        self.mongoUtils.clear_all(db)

    def __del__(self):
        self.mongoUtils.close_conn()

if __name__ == '__main__':
    input = raw_input('clear all data, really? (y/n):')
    if input.lower()=='y':
        initUtils=InitUtils()
        initUtils.init()
    else:
        print 'Noting be clear, bye!'
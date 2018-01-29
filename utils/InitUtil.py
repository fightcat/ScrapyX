# -*- coding: utf-8 -*-
'''
@author: tieqiang Xu
@mail: 805349916@qq.com
'''

from utils.MongoUtils import MongoUtils
#import sys
import configs.Settings as Settings

class InitUtil:
    '''
    初始化，清空所有数据，重新开始新一轮任务
    '''
    def __init__(self):
        self.mongoUtils = MongoUtils()
        pass

    def init(self):
        db = Settings.MONGO_DB
        self.mongoUtils.clear_all(db)

    def __del__(self):
        self.mongoUtils.close_conn()

if __name__ == '__main__':
    input = input('clear all data, really? (y/n):')
    if input.lower()=='y':
        #initUtils=InitUtils()
        #initUtils.init()
        print('all data clear finished')
    else:
        print('Noting be clear, bye!')

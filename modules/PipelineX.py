# -*- coding: utf-8 -*-
'''
@author: tieqiang Xu
@mail: 805349916@qq.com
'''

import sys

from utils.LogUtils import log
from utils.TaskUtils import TaskUtils
from utils.MongoUtils import MongoUtils

class PipelineX:
    '''
    存储结果管道
    （不负责压next task）
    '''
    def __init__(self,task):
        self.task = task
        self.taskUtils = TaskUtils()
        self.mongoUtils = MongoUtils()
        pass

    def run(self):
        '''
        分发
        :return: 无
        '''
        log.i ('Pipeline.run()')
        if self.task['parser'] == 'demo':
            self.save_info('demo_info')
        else:
            pass
        #将本条task的状态置为done
        if '_id' in self.task.keys():
            self.taskUtils.set_state(self.task['_id'],'done')
        pass

    def save_info(self,collection_name):
        '''
        存储demo
        demo_info
        {
            '_id':'http://tieba.baidu.com',
            'name':'百度贴吧'
        }
        :return:
        '''
        if self.task['parent'] is None:
            self.task['parent']={}
        if self.task['results'] is not None:
            for result in self.task['results']:
                insert_data = dict(self.task['parent'], **result)
                self.mongoUtils.insert(collection_name=collection_name,insert_data=insert_data)
        pass


    def __del__(self):
        self.mongoUtils.close_conn()

if __name__ == '__main__':
    task={
        'state': 'doing',
        'parser': 'phase',
        'request': 'http://www.baidu.com',
        'parent':{},
        'response':''
    }
    pipeline = PipelineX(task)
    pipeline.run()
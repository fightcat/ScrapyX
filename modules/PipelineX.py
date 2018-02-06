# -*- coding: utf-8 -*-
'''
@author: tieqiang Xu
@mail: 805349916@qq.com
'''

import sys

from utils.LogUtil import Log
from utils.TaskUtil import TaskUtil
from utils.MongoUtil import MongoUtil

class Pipeline():
    '''
    存储结果管道
    （不负责压next task）
    '''
    def __init__(self,task):
        self.task = task
        self.taskUtil = TaskUtil()
        self.mongoUtil = MongoUtil()
        pass

    def run(self):
        '''
        分发
        :return: 无
        '''
        Log.i ('Pipeline.run()')
        if self.task['results'] is not None and len(self.task['results'])>0:
            #下次任务入队列
            if 'next_tasks' in self.task and self.task['next_tasks'] is not None:
                for next_task in self.task['next_tasks']:
                    self.taskUtil.insert_one(next_task)
            #本次解析结果入库
            # 利用反射机制自动执行pipeline_<parser名>（）函数，如果找不到则执行默认的pipeline_default()函数
            if hasattr(self, 'pipeline_' + self.task['parser']):
                func = getattr(self, 'pipeline_' + self.task['parser'])
                func(self.task['table'])
            else:
                self.pipeline_default(self.task['table'])
            #将完整task存入mongo，并将本条task
            self.task['state']='done'
            self.taskUtil.replace_one(self.task['_id'], self.task)
        else:
            #没有解析出结果，则表示中间出错了，等待下次再启动
            pass
        Log.i('this task is finished')

    def pipeline_default(self,collection_name):
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
                self.mongoUtil.insert(collection_name=collection_name,insert_data=insert_data)
        pass


    def __del__(self):
        self.mongoUtil.close_conn()

if __name__ == '__main__':
    task={
        'state': 'doing',
        'parser': 'phase',
        'request': 'http://www.baidu.com',
        'parent':{},
        'response':''
    }
    pipelineX = Pipeline(task)
    pipelineX.run()
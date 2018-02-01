# -*- coding: utf-8 -*-
'''
@author: tieqiang Xu
@mail: 805349916@qq.com
'''
import importlib
from configs import Setting
from utils.LogUtil import Log
from utils.TaskUtil import TaskUtil


class Parser():
    '''
    Html解析器
    '''
    def __init__(self,task):
        self.task = task
        self.taskUtil = TaskUtil()

    def run(self):
        '''
        分发
        :return:
        '''
        Log.i ('Parser.run()')
        # 利用反射机制自动执行parse_<parser名>（）函数，如果找不到则执行默认的parse_default()函数
        if hasattr(self, 'parse_' + self.task['parser']):
            func = getattr(self, 'parse_' + self.task['parser'])
            func()
        else:
            self.parse_default()
        #启动Pipeline
        pipelineModule = Setting.PIPELINE_MODULE
        PipelineX = importlib.import_module(pipelineModule)
        pipeline = PipelineX.Pipeline(self.task)
        pipeline.run()

    def parse_default(self):
        Log.i('run default parser ')
        pass

if __name__ == '__main__':
    task ={
        'state': 'doing',
        'parser': 'demo',
        'request': 'http://www.baidu.com',
        'response': '<html></html>'
    }
    parserX=Parser(task)
    parserX.run()

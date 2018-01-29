# -*- coding: utf-8 -*-
'''
@author: tieqiang Xu
@mail: 805349916@qq.com
'''
from lxml import etree

from modules.PipelineX import PipelineX
from utils.LogUtil import Log
from utils.TaskUtil import TaskUtil


class ParserX:
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
        pipelineX=PipelineX(self.task)
        pipelineX.run()

    def parse_demo(self):
        '''
        解析demo
        :return:
        '''
        root = etree.HTML(self.task['response'])
        nodes = root.xpath('//a[contains(@class,"nav")]')
        items=[]
        next_tasks=[]
        for node in nodes:
            #解析学段
            item={}
            item['_id'] = node.get('href')
            item['name'] = node.text
            items.append(item)
            #解析下一任务,并插入任务队列
            next_task={
                'parser': 'next',
                'request': node.get('href'),
                'table': 'next_info',
                'parent': {
                    'parent_id':item['_id'],
                    'parent_name':item['name']
                }
            }
            next_tasks.append(next_task)
        #解析结果和下次任务存入task
        self.task['results']=items
        self.task['next_tasks']=next_tasks

    def parse_default(self):
        pass

if __name__ == '__main__':
    task ={
        'state': 'doing',
        'parser': 'demo',
        'request': 'http://www.baidu.com',
        'response': '<html></html>'
    }
    parserX=ParserX(task)
    parserX.run()

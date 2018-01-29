# -*- coding: utf-8 -*-
'''
@author: tieqiang Xu
@mail: 805349916@qq.com
'''
from lxml import etree

from modules.Pipeline import Pipeline
from utils.LogUtils import log
from utils.TaskUtils import TaskUtils


class ParserX:
    '''
    Html解析器
    '''
    def __init__(self,task):
        self.task = task
        self.taskUtils = TaskUtils()

    def run(self):
        '''
        分发
        :return:
        '''
        log.i ('Parser.run()')
        if self.task['parser'] in ['demo']:
            self.parse_demo()
        else:
            pass

        pipeline=Pipeline(self.task)
        pipeline.run()


    def parse_demo(self):
        '''
        解析demo
        :return:
        '''
        root = etree.HTML(self.task['response'])
        nodes = root.xpath('//a[contains(@class,"nav")]')
        items=[]
        for node in nodes:
            #解析学段
            item={}
            item['_id'] = node.get('href')
            item['name'] = node.text
            items.append(item)
            #解析下一任务,并插入任务队列
            parent = {
                'parent_id':item['_id'],
                'parent_name':item['name']
            }
            self.taskUtils.insert_one(parser='next',request=node.get('href'),parent=parent)
        #解析结果存入task
        self.task['results']=items

if __name__ == '__main__':
    task ={
        'state': 'doing',
        'parser': 'demo',
        'request': 'http://www.baidu.com',
        'response': '<html></html>'
    }
    parser=ParserX(task)
    parser.run()
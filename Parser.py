# coding:utf-8
'''
Html解析器
'''
import sys
import BeautifulSoup
from lxml import etree
from utils.TaskUtils import TaskUtils
from Pipeline import Pipeline
import re
import json

class Parser:

    def __init__(self,task):
        reload(sys)
        sys.setdefaultencoding('utf-8');
        self.task = task
        self.taskUtils = TaskUtils()

    def run(self):
        '''
        分发
        :return:
        '''
        print 'Parser.run()'
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
        html = etree.HTML(self.task['response'])
        nodes = html.xpath('//a[contains(@class,"nav")]')
        items=[]
        for node in nodes:
            #解析学段
            item={}
            item['_id'] = node.get('href')
            item['name'] = node.text.encode('utf-8')
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
    parser=Parser(task)
    parser.run()
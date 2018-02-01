# -*- coding: utf-8 -*-
'''
@author: tieqiang Xu
@mail: 805349916@qq.com
'''
from  modules.ParserX import Parser
from utils.RegexpUtil import RegexpUtil
from utils.XpathUtil import XpathUtil


class Parser(Parser):

    def parse_demo(self):
        '''
        解析self.task['response']，将结果存入self.task['results']，将下次任务存入self.task['next_tasks']
        :return: 无
        '''
        root = XpathUtil.getRoot(self.task['response'])
        nodes = XpathUtil.getNodes(root,'//a[contains(@class,"nav")]')
        items=[]
        next_tasks=[]
        for node in nodes:
            #解析学段
            item={}
            item['href'] = XpathUtil.htmltrim(node.get('href'))
            item['name'] = XpathUtil.htmltrim(node.text)
            item['_id'] = RegexpUtil.substring(item['href'],'http\:\/\/','\.com')
            items.append(item)
            #解析下一任务,并插入任务队列
            next_task={
                'parser': 'next',
                'request': item['_id'],
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

if __name__ == '__main__':
    pass

# coding:utf-8
"""
Task操作工具
tasks
{
    "parser": "phase"
    "request": "http://so.eduyun.cn/synResource",
    "response": "<html>...</html>"
    "parent": {},
    "state": "done",
    "uptime":
}
"""

from MongoUtils import MongoUtils
import os
import configs.Settings as Settings

class TaskUtils:

    def __init__(self):
        self.mongoUtils = None
        self.mongoUtils = MongoUtils()
        count=self.mongoUtils.count(collection_name='tasks')
        if count==0:
            first_task_parser = Settings.FIRST_TASK_PARSER
            first_task_url = Settings.FIRST_TASK_URL
            insert_data = {
                "parser": first_task_parser,
                "request": first_task_url,
                "parent":{},
                "state": "ready"
            }
            self.mongoUtils.insert(collection_name='tasks', insert_data=insert_data)

    def get_ready(self):
        '''
        获取一条待执行的任务（准备状态）
        :return: dict 单条任务
        '''
        # 过滤条件，不存在state字段或state=ready
        filter_dict = {
            '$or': [
                {
                    'state': {'$exists': False}
                },
                {
                    'state': 'ready'
                }
            ]
        }
        # 执行mongo操作
        task = self.mongoUtils.find_one(collection_name='tasks', filter_dict=filter_dict)
        return task

    def set_state(self,id,state):
        '''
        设置任务状态(ready，doing，done)
        :param id: str 主键id
        :param state: str 更新状态值
        :return: 无
        '''
        filter_dict = {'_id':id}
        update_dict = {
            '$set':{'state':state}
        }
        self.mongoUtils.update(collection_name='tasks', filter_dict=filter_dict, update_dict=update_dict)

    def update_all(self,id,task):
        '''
        更新整个任务
        :param id: str
        :param task: dict
        :return: 无
        '''

    def insert_one(self, parser, request ,parent):
        '''
        插入一条task
        :param parser: str 解析器
        :param request: str 请求的url
        :return: 无
        '''
        filter_dict={
            'parser': parser,
            'request': request,
            'parent': parent
        }
        r = self.mongoUtils.find_one(collection_name='tasks', filter_dict=filter_dict)
        if r is None:
            task = {
                'parser': parser,
                'request': request,
                'parent': parent,
                'state': 'ready'
            }
            r=self.mongoUtils.insert(collection_name='tasks', insert_data=task)

    def __del__(self):
        self.mongoUtils.close_conn()
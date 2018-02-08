# -*- coding: utf-8 -*-
'''
@author: tieqiang Xu
@mail: 805349916@qq.com
'''
import json

from utils.MongoUtil import MongoUtil
import os
import configs.Setting as Setting

class TaskUtil:
    '''
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
    '''
    def __init__(self):
        self.mongoUtil = MongoUtil()
        count=self.mongoUtil.count(collection_name='tasks')
        if count==0:
            task=None
            task_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'configs', 'task.json')
            f = open(task_file,encoding='utf-8')
            task=f.read()
            f.close()
            insert_data=json.loads(task)
            self.mongoUtil.insert(collection_name='tasks', insert_data=insert_data)

    def get_ready(self):
        '''
        获取一条待执行的任务（准备状态），并置为doing状态
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
        # 更新条件，将state=doing
        update_dict={
            '$set':{
                'state':'doing'
            }
        }
        # 执行mongo操作
        task = self.mongoUtil.find_one_and_update(collection_name='tasks', filter_dict=filter_dict, update_dict=update_dict)
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
        self.mongoUtil.update(collection_name='tasks', filter_dict=filter_dict, update_dict=update_dict)

    def replace_one(self, id, task):
        '''
        更新整个任务
        :param id: str
        :param task: dict
        :return: 无
        '''
        filter_dict={
            '_id':id
        }
        r=self.mongoUtil.find_one_and_replace(collection_name='tasks', filter_dict=filter_dict, replace_dict=task)
        return r

    def insert_one(self, task):
        '''
        插入一条task
        :param parser: str 解析器
        :param request: str 请求的url
        :return: 无
        '''
        r = self.mongoUtil.find_one(collection_name='tasks', filter_dict=task)
        if r is None:
            task['state']='ready'
            r=self.mongoUtil.insert(collection_name='tasks', insert_data=task)

    def __del__(self):
        self.mongoUtil.close_conn()
# -*- coding: utf-8 -*-
'''
@author: tieqiang Xu
@mail: 805349916@qq.com
'''

import os
from pymongo import MongoClient
from pymongo import ReturnDocument
import configs.Setting as Setting
import time
import datetime
import traceback
from utils.LogUtil import Log

class MongoUtil():
    '''
    mongo操作工具
    '''
    def __init__(self, host=None, port=None, db_name=None, mechanism=None, user=None, password=None):
        """
        初始化对象，链接数据库
        :param host: mongo数据库所在服务器地址
        :param port: mongo数据库端口
        :param db_name: 数据库的名称
        :param mechanism: 认证类型，None：无认证，MONGODB-CR：2.x认证，SCRAM-SHA-1：3.x认证
        :param user：用户名
        :param password：密码
        :return: 无返回值
        """
        if host is None:
            host=Setting.MONGO_HOST
        if port is None:
            port = Setting.MONGO_PORT
        if db_name is None:
            db_name = Setting.MONGO_DB
        if mechanism is None:
            mechanism = Setting.MONGO_MECHANISM
        if user is None:
            user=Setting.MONGO_USER
        if password is None:
            password=Setting.MONGO_PASSWORD
        try:
            Log.d('start connect mongo')
            self.client = None
            self.client = MongoClient(host, int(port))
            self.database = self.client.get_database(db_name)
            if mechanism is not None:
                self.database.authenticate(user,password,mechanism=mechanism)
            Log.d('mongo connect success')
        except Exception as e:
            self.close_conn()
            Log.e('init mongo bar failed: %s' % e)

    def count(self, collection_name, filter_dict=None):
        """
        查找表记录条数，默认返回0
        :param collection_name: str 集合名
        :param table_name: str 表名
        :param filter_dict: dict 过滤条件
        :return: int 表记录条数
        """
        tab_size = 0
        try:
            collection = self.database.get_collection(collection_name)
            tab_size = collection.find(filter_dict).count()
            return tab_size
        except Exception as e:
            Log.e('get table size failed: %s' % e)
        finally:
            return tab_size

    def update(self, collection_name, filter_dict, update_dict, insert=False, multi=False, auto_uptime=True):
        """
        更新表记录，默认返回false
        :param collection_name: str 集合名
        :param filter_dict: dict 过滤条件，如{'campaignId':{'$in':[1,2,3]}}
        :param update_dict: dict 更新的字段，如{'$set':{'status_key:0','campaign.status':1},{'$unset':'campaign.name':'test_camp'}}
        :param insert: bool 如果需要更新的记录不存在是否插入
        :param multi: bool 是否更新所有符合条件的记录， False则只更新一条，True则更新所有
        :return: bool 是否更新成功
        """
        result = False
        try:
            if auto_uptime:
                timestamp = time.time()
                uptimestamp = int(round(timestamp * 1000))
                uptime = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                if '$set' in update_dict:
                    update_dict['$set']['uptime']=uptime
                    update_dict['$set']['uptimestamp'] = uptimestamp
                else:
                    update_dict['$set']={'uptime':uptime,'uptimestamp':uptimestamp}
            collection = self.database.get_collection(collection_name)
            collection.update(filter_dict, update_dict, insert, multi)
            result = True
            Log.d("update success!")
        except Exception as e:
            Log.e('update failed: %s' % e)
            traceback.print_exc()
        finally:
            return result

    def insert(self, collection_name, insert_data,auto_uptime=True):
        """
        更新表记录，默认返回false
        :param collection_name: str 集合名
        :param insert_data: dict 插入的数据，如{'campaignId':{'$in':[1,2,3]}}
        :return: bool 是否更新成功
        """
        result = False
        try:
            if auto_uptime:
                timestamp = time.time()
                uptimestamp = int(round(timestamp * 1000))
                uptime = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                if type(insert_data)==dict:
                    insert_data['uptime'] = uptime
                    insert_data['uptimestamp'] = uptimestamp
                elif type(insert_data)==list:
                    items=[]
                    for data in insert_data:
                        data['uptime'] = uptime
                        data['uptimestamp'] = uptimestamp
                        items.append(data)
                    insert_data=items
            collection = self.database.get_collection(collection_name)
            collection.insert(insert_data)
            result = True
            Log.d("insert success!")
        except Exception as e:
            Log.e('insert failed: %s' % e)
        finally:
            return result

    def delete(self, collection_name, filter_dict):
        """
        更新表记录，默认返回false
        :param collection_name: str 集合名
        :param filter_dict: dict 查询条件，如{'campaignId':{'$in':[1,2,3]}}
        :return: bool 是否更新成功
        """
        result = False
        try:
            collection = self.database.get_collection(collection_name)
            collection.remove(filter_dict)
            result = True
            Log.d("remove success!")
        except Exception as e:
            Log.e('remove failed: %s' % e)
        finally:
            return result

    def replace(self,collection_name, filter_dict, replace_data,auto_uptime=True):
        """
        替换文档，默认返回false
        :param collection_name: str 集合名
        :param filter_dict: dict 查询条件，如{'campaignId':{'$in':[1,2,3]}}
        :param replace_data: dict 替换的数据，如{'campaignId':{'$in':[4,5,6]}}
        :return: bool 是否更新成功
        """
        result = False
        try:
            if auto_uptime:
                timestamp = time.time()
                uptimestamp = int(round(timestamp * 1000))
                uptime = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                replace_data['uptime'] = uptime
                replace_data['uptimestamp'] = uptimestamp
            collection = self.database.get_collection(collection_name)
            collection.replace_one(filter_dict,replace_data)
            result = True
            Log.d("remove success!")
        except Exception as e:
            Log.e('remove failed: %s' % e)
        finally:
            return result


    def find_one(self, collection_name, filter_dict=None, projection_dict=None):
        """
        查找一条表记录，默认返回空字典
        :param collection_name: str 集合名
        :param filter_dict: dict 过滤条件如{'campaignId':123}
        :param projection_dict: dict 返回的字段如{'campaign.status':1,'updated':1,'_id':0}
        :return: dict 查找到的数据
        """
        result = {}
        try:
            collection = self.database.get_collection(collection_name)
            result = collection.find_one(filter_dict, projection_dict)
        except Exception as e:
            Log.e('find data failed: %s' % e)
        finally:
            return result

    def find_many(self, collection_name, filter_dict=None, projection_dict=None, limit_size=0, skip_index=0):
        """
        查找多条表记录，默认返回空数组
        :param collection_name: str 集合名
        :param filter_dict: dict filter_dict: 过滤条件如{'campaignId':123}
        :param projection_dict: dict 返回的字段如{'campaign.status':1,'updated':1,'_id':0}
        :param limit_size: int 限定返回的数据条数
        :param skip_index: int 游标位移
        :return: list 查询到的记录组成的列表，每个元素是一个字典
        """
        result = []
        try:
            collection = self.database.get_collection(collection_name)
            if not limit_size:
                if not skip_index:
                    result = collection.find(filter_dict, projection_dict)
                else:
                    result = collection.find(filter_dict, projection_dict).skip(skip_index)
            else:
                if not skip_index:
                    result = collection.find(filter_dict, projection_dict).limit(limit_size)
                else:
                    result = collection.find(filter_dict, projection_dict).skip(skip_index).limit(limit_size)
        except Exception as e:
            Log.e('find data failed: %s' % e)
        finally:
            return result

    def find_one_and_update(self, collection_name, filter_dict, update_dict, upsert=False, auto_uptime=True):
        """
        查找并更新表记录，默认返回false，保证原子性
        :param collection_name: str 集合名
        :param filter_dict: dict 过滤条件，如{'campaignId':{'$in':[1,2,3]}}
        :param update_dict: dict 更新的字段，如{'$set':{status_key:0，'campaign.status':1},{'$unset':'campaign.name':'test_camp'}}
        :param insert: bool 如果需要更新的记录不存在是否插入
        :param multi: bool 是否更新所有符合条件的记录， False则只更新一条，True则更新所有
        :return: Document 更新成功后的文档
        """
        result = None
        try:
            if auto_uptime:
                timestamp = time.time()
                uptimestamp = int(round(timestamp * 1000))
                uptime = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                if '$set' in update_dict:
                    update_dict['$set']['uptime'] = uptime
                    update_dict['$set']['uptimestamp'] = uptimestamp
                else:
                    update_dict['$set'] = {'uptime': uptime, 'uptimestamp': uptimestamp}
            collection = self.database.get_collection(collection_name)
            document=collection.find_one_and_update(filter_dict, update_dict, upsert=upsert,return_document=ReturnDocument.AFTER)
            result = document
            if result is None:
                Log.i("[INFO] find and update nothing!")
            else:
                Log.d("[INFO] find and update success!")
        except Exception as e:
            Log.e('find and update failed: %s' % e)
        finally:
            return result

    def find_one_and_replace(self, collection_name, filter_dict, replace_dict, upsert=False, auto_uptime=True):
        """
        查找并更新表记录，默认返回false，保证原子性
        :param collection_name: str 集合名
        :param filter_dict: dict 过滤条件，如{'campaignId':{'$in':[1,2,3]}}
        :param update_dict: dict 更新的字段，如{'$set':{status_key:0，'campaign.status':1},{'$unset':'campaign.name':'test_camp'}}
        :param insert: bool 如果需要更新的记录不存在是否插入
        :param multi: bool 是否更新所有符合条件的记录， False则只更新一条，True则更新所有
        :return: Document 更新成功后的文档
        """
        result = None
        try:
            if auto_uptime:
                timestamp = time.time()
                uptimestamp = int(round(timestamp * 1000))
                uptime = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                replace_dict['uptime']=uptime
                replace_dict['uptimestamp'] = uptimestamp
            collection = self.database.get_collection(collection_name)
            document=collection.find_one_and_replace(filter_dict, replace_dict, upsert=upsert,return_document=ReturnDocument.AFTER)
            result = document
            if result is None:
                Log.i("[INFO] find and update nothing!")
            else:
                Log.d("[INFO] find and update success!")
        except Exception as e:
            Log.e('find and update failed: %s' % e)
        finally:
            return result

    def clear_all(self,db_name):
        '''
        删除数据库
        :return:
        '''
        self.client.drop_database(db_name);

    def close_conn(self):
        """
        关闭数据库链接
        :return: 无返回值
        """
        if self.client:
            self.client.close()
            Log.d('closed mongo connection')

    def __del__(self):
        '''
        析构方法
        :return: 无
        '''
        self.close_conn()

if __name__ == '__main__':
    '''
    update_dict={}
    #update_dict={'$set': {'uptime': '2018-01-25 17:38:33.522000', 'uptimestamp': 1516873113997000.0}}
    mongoUtils= MongoUtils()
    #cnt=mongoUtils.count('tasks')
    #print cnt
    mongoUtils.update(collection_name='res_demo',filter_dict={},update_dict=update_dict)
    '''
    insert_data=[{'uptime': '2018-01-25 17:38:33.522000', 'uptimestamp': 1516873113997000.0}]

    mongoUtils = MongoUtil()
    mongoUtils.insert(collection_name='res_demo',insert_data=insert_data)


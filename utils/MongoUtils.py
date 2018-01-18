# coding:utf-8
"""
mongo操作工具
"""
import os
from pymongo import MongoClient
from PropertiesUtils import PropertiesUtils

class MongoUtils():

    def __init__(self, host=None, port=None, db_name=None):
        """
        初始化对象，链接数据库
        :param host: mongo数据库所在服务器地址
        :param port: mongo数据库端口
        :param db_name: 数据库的名称
        :return: 无返回值
        """
        conf_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configs.properties')
        propertiesUtils = PropertiesUtils(conf_file)
        if host is None:
            host=propertiesUtils.getValue('MONGO_HOST')
        if port is None:
            port = propertiesUtils.getValue('MONGO_PORT')
        if db_name is None:
            db_name = propertiesUtils.getValue('MONGO_DB')
        try:
            self.client = None
            self.client = MongoClient(host, int(port))
            self.database = self.client.get_database(db_name)
        except Exception as e:
            self.close_conn()
            print('init mongo bar failed: %s' % e)

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
            print('get table size failed: %s' % e)
        finally:
            return tab_size

    def update(self, collection_name, filter_dict, update_dict, insert=False, multi=False):
        """
        更新表记录，默认返回false
        :param collection_name: str 集合名
        :param filter_dict: dict 过滤条件，如{'campaignId':{'$in':[1,2,3]}}
        :param update_dict: dict 更新的字段，如{'$set':{status_key:0，'campaign.status':1},{'$unset':'campaign.name':'test_camp'}}
        :param insert: bool 如果需要更新的记录不存在是否插入
        :param multi: bool 是否更新所有符合条件的记录， False则只更新一条，True则更新所有
        :return: bool 是否更新成功
        """
        result = False
        try:
            collection = self.database.get_collection(collection_name)
            collection.update(filter_dict, update_dict, insert, multi)
            result = True
            print("[INFO] update success!")
        except Exception as e:
            print('update failed: %s' % e)
        finally:
            return result

    def insert(self, collection_name, insert_data):
        """
        更新表记录，默认返回false
        :param collection_name: str 集合名
        :param insert_data: dict 插入的数据，如{'campaignId':{'$in':[1,2,3]}}
        :return: bool 是否更新成功
        """
        result = False
        try:
            collection = self.database.get_collection(collection_name)
            collection.insert(insert_data)
            result = True
            print("insert success!")
        except Exception as e:
            print('insert failed: %s' % e)
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
            print("remove success!")
        except Exception as e:
            print('remove failed: %s' % e)
        finally:
            return result

    def replace(self,collection_name, filter_dict, replace_data):
        """
        替换文档，默认返回false
        :param collection_name: str 集合名
        :param filter_dict: dict 查询条件，如{'campaignId':{'$in':[1,2,3]}}
        :param replace_data: dict 替换的数据，如{'campaignId':{'$in':[4,5,6]}}
        :return: bool 是否更新成功
        """
        result = False
        try:
            collection = self.database.get_collection(collection_name)
            collection.replace_one(filter_dict,replace_data)
            result = True
            print("remove success!")
        except Exception as e:
            print('remove failed: %s' % e)
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
            print('find data failed: %s' % e)
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
            print('find data failed: %s' % e)
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
            print 'closed mongo connection'

if __name__ == '__main__':
    mongoUtils= MongoUtils()
    cnt=mongoUtils.count('tasks')
    print cnt

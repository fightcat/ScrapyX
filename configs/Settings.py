# coding:utf-8
'''
设置项，运行时不可变
'''

#Mongodb配置(主机、端口、数据库名)
MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_DB = 'res_demo'
MONGO_MECHANISM =None  #None：无认证，MONGODB-CR：2.x认证，SCRAM-SHA-1：3.x认证
MONGO_USER = ''
MONGO_PASSWORD = ''

#Task配置(初始任务的解析器、Url)
FIRST_TASK_PARSER = 'demo'
FIRST_TASK_URL = 'http://www.baidu.com'

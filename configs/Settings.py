# -*- coding: utf-8 -*-
'''
设置项，运行时不可变

@author: tieqiang Xu
@mail: 805349916@qq.com
'''

#Mongodb配置(主机、端口、数据库名)
MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
#Mongo数据库名
MONGO_DB = 'res_demo'
#访问Mongo的MONGO_DB数据库的MECHANISM认证。None：无认证，MONGODB-CR：2.x认证，SCRAM-SHA-1：3.x认证
MONGO_MECHANISM =None
#访问Mongo的MONGO_DB数据库的用户名和密码
MONGO_USER = ''
MONGO_PASSWORD = ''

#初始Task配置(初始任务的解析器、Url，由Scheduler在调用TaskUtil的构造方法时调用创建第1个Task)
FIRST_TASK_PARSER = 'demo'
FIRST_TASK_URL = 'http://www.baidu.com'

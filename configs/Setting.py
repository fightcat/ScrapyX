# -*- coding: utf-8 -*-
'''
设置项，运行时不可变

@author: tieqiang Xu
@mail: 805349916@qq.com
'''
##############
# Mongodb配置
##############
#Mongo主机和端口
MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
#Mongo数据库名
MONGO_DB = 'res_demo'
#访问Mongo的MONGO_DB数据库的MECHANISM认证。None：无认证，MONGODB-CR：2.x认证，SCRAM-SHA-1：3.x认证
MONGO_MECHANISM =None
#访问Mongo的MONGO_DB数据库的用户名和密码
MONGO_USER = ''
MONGO_PASSWORD = ''

###############
# 模块配置
###############
SCHEDULER_MODULE = 'modules.SchedulerX'
DOWNLOADER_MODULE = 'modules.DownloaderX'
#PARSER_MODULE = 'modules.ParserX'
PARSER_MODULE = 'demo.ParserDemo'
PIPELINE_MODULE = 'modules.PipelineX'

####################
# Http request参数
####################
# http代理服务器配置，类型string，例如：127.0.0.1:8888
HTTP_PROXY = None
# http user_agent，类型string
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
# http cookies，类型string，例如：_ga=GA1.2.693027078.1517447891; _gid=GA1.2.390668217.1517447891
COOKIES = None
# http referer，类型string，例如：http://www.cnblogs.com/zy6103/p/
REFERER = None
# response的charset，类型string，根据网页的字符集设置，例如：utf-8、gb2312，GBK等
CHARSET= 'utf-8'

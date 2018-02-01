# -*- coding: utf-8 -*-
'''
@author: tieqiang Xu
@mail: 805349916@qq.com
'''

import time
import datetime
import os
import sys
import threading
from queue import Queue
from pymongo import MongoClient
from configs import Setting
from utils.ConfigUtil import ConfigUtil


class Log():
    '''
    日志处理类，输出到console和mongodb
    DEBUG,INFO, WARN，ERROR
    '''
    @staticmethod
    def d(text):
        '''
        输出debug信息
        :param text: 日志文本
        :return: 无
        '''
        fileName = os.path.basename(sys._getframe().f_back.f_code.co_filename)
        funcName = sys._getframe().f_back.f_code.co_name  # 获取调用函数名
        lineNumber = sys._getframe().f_back.f_lineno  # 获取行号
        Log._print('DEBUG', funcName + '(),' + fileName + ':' + str(lineNumber), text)
        pass

    @staticmethod
    def i(text):
        '''
        输出info信息
        :param text: 日志文本
        :return: 无
        '''
        fileName = os.path.basename(sys._getframe().f_back.f_code.co_filename)
        funcName = sys._getframe().f_back.f_code.co_name  # 获取调用函数名
        lineNumber = sys._getframe().f_back.f_lineno  # 获取行号
        Log._print('INFO', funcName + '(),' + fileName + ':' + str(lineNumber), text)
        pass

    @staticmethod
    def w(text):
        '''
        输出warn信息
        :param text: 日志文本
        :return: 无
        '''
        fileName = os.path.basename(sys._getframe().f_back.f_code.co_filename)
        funcName = sys._getframe().f_back.f_code.co_name  # 获取调用函数名
        lineNumber = sys._getframe().f_back.f_lineno  # 获取行号
        Log._print('WARN', funcName + '(),' + fileName + ':' + str(lineNumber), text)
        pass

    @staticmethod
    def e(text):
        '''
        输出error信息
        :param text:
        :return:
        '''
        fileName = os.path.basename(sys._getframe().f_back.f_code.co_filename)
        funcName = sys._getframe().f_back.f_code.co_name  # 获取调用函数名
        lineNumber = sys._getframe().f_back.f_lineno  # 获取行号
        Log._print('ERROR', funcName + '(),' + fileName + ':' + str(lineNumber), text)
        pass

    @staticmethod
    def _print(level,source,text):
        '''
        打印
        :param self:
        :return: 无
        '''
        timestamp = time.time()
        log_timestamp = int(round(timestamp * 1000))
        log_timestring = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        pid=os.getpid()
        #将log写入console
        config_level = ConfigUtil.get('log', 'level')
        enum_level=['DEBUG', 'INFO', 'WARN', 'ERROR']
        level_index=enum_level.index(level) if level in enum_level else -1
        config_level_index=enum_level.index(config_level) if config_level in enum_level else -1
        if level_index >= config_level_index and level_index>=0 and config_level_index>=0:
            print('[%s] [%s] [%d] [%s]: %s' % (log_timestring,level,pid,source,text))
        #启动线程将log写入mongodb的logs集合
        logdict={
            'timestamp':log_timestamp,
            'timestring':log_timestring,
            'level':level,
            'pid':pid,
            'source':source,
            'text':text
        }
        mongoLog.put_queue(logdict)
        pass


class _MongoLog(threading.Thread):
    '''
    Mongodb写log类
    '''
    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = Queue()

    def put_queue(self,log):
        self.queue.put(log)

    def run(self):
        while True:
            try:
                insert_data=self.queue.get(block=False)
                self._insert(insert_data=insert_data)
            except  Exception as e:
                exit_flag=getattr(Setting,'exit_flag',False)
                if exit_flag:
                    break
                else:
                    time.sleep(1)
            finally:
                pass
        pass

    def _insert(self,insert_data):
        '''
        将日志插入Mongo，
        注意不能直接调用MongoUtils，因为MongoUtils和log有循环引用,会导致相互调用无限插入
        :param insert_data: 日志数据
        :return: 无
        '''
        host=Setting.MONGO_HOST
        port = Setting.MONGO_PORT
        db_name = Setting.MONGO_DB
        mechanism = Setting.MONGO_MECHANISM
        user=Setting.MONGO_USER
        password=Setting.MONGO_PASSWORD
        client = None
        try:
            client = MongoClient(host, int(port))
            database = client.get_database(db_name)
            if mechanism is not None:
                database.authenticate(user,password,mechanism=mechanism)
            collection = database.get_collection("logs")
            collection.insert(insert_data)
        finally:
            if client:
                client.close()

#创建单例对象(内含对列)
mongoLog=_MongoLog()
mongoLog.start()

def test():
    Log.d("hello world你好")
    #Log.i("hello world你好你好")
    #Log.w("hello world你好你好你好")
    #Log.e("hello world你好你好你好你好")

if __name__ == '__main__':
    test()

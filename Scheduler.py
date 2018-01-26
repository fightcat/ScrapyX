# -*- coding: utf-8 -*-
'''
调度器，
1.从队列中取task
2.向队列中压task
3.修改task状态
'''

import time
from utils.TaskUtils import TaskUtils
from Downloader import Downloader
import os
from utils.ConfigUtils import ConfigUtils
import random
from multiprocessing import Pool

class Scheduler:
    def __init__(self):
        self.taskUtils = None
        self.taskUtils = TaskUtils()
        pass

    @staticmethod
    def run_downloader(task):
        '''
        运行Downloader下载器(必须为静态方法，以便被multiprocessingPool异步调用)
        :param task:
        :return:
        '''
        downloader = Downloader(task)
        downloader.run()

    def run(self):
        '''
        每隔1秒，循环读取tasks
        交给Downloader
        :return:
        '''
        #创建进程池
        pool=Pool()
        while True:
            #获取一条待执行的Task,并置为doing状态
            task = self.taskUtils.get_ready()
            if task is not None and len(task)>0 or True:
                print ('-----------------------------')
                #用进程池启动Downloader
                pool.apply_async(self.run_downloader, args=(task,))
            #休眠n秒(从配置文件中读取)
            items=ConfigUtils.getItems('scheduler')
            interval_min = items['interval_min']
            interval_max = items['interval_max']
            seconds=random.randint(int(interval_min),int(interval_max))
            time.sleep(seconds)
        pool.close()
        pool.join()
        print ('All subprocesses done.')

if __name__ == '__main__':
    scheduler=Scheduler()
    scheduler.run()
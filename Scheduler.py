# coding:utf-8
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
from utils.PropertiesUtils import PropertiesUtils
import random

class Scheduler:
    def __init__(self):
        self.taskUtils = None
        self.taskUtils = TaskUtils()
        pass

    def run(self):
        '''
        每隔1秒，循环读取tasks
        交给Downloader
        :return:
        '''
        while True:
            #获取一条待执行的Task
            task = self.taskUtils.get_ready()
            print(task)
            if task is not None and len(task)>0:
                #更新task的state
                self.taskUtils.set_state(task['_id'],'doing')
                #启动Downloader线程
                downloader=Downloader(task)
                downloader.start()
            #休眠n秒(从配置文件中读取)
            conf_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'utils','configs.properties')
            propertiesUtils = PropertiesUtils(conf_file)
            scheduler_interval_min = propertiesUtils.getValue('scheduler_interval_min')
            scheduler_interval_max = propertiesUtils.getValue('scheduler_interval_max')
            seconds=random.randint(int(scheduler_interval_min),int(scheduler_interval_max))
            time.sleep(seconds)

if __name__ == '__main__':
    scheduler=Scheduler()
    scheduler.run()
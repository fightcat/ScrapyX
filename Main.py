# -*- coding: utf-8 -*-
'''
爬虫入口
@author: tieqiang Xu
@mail: 805349916@qq.com
'''
import sys
from Scheduler import Scheduler

def main():
    #执行任务计划
    scheduler = Scheduler()
    scheduler.run()

if __name__ == '__main__':
    #项目入口
    main()
    sys.exit(0)
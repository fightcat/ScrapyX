# coding:utf-8
'''
爬虫入口
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
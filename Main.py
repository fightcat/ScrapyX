# coding:utf-8
'''
爬虫入口
'''
import sys
from Scheduler import Scheduler

def main():
    #设置环境变量，默认编码为utf-8，解决各种乱码问题
    reload(sys)
    sys.setdefaultencoding('utf-8');
    #执行任务计划
    scheduler = Scheduler()
    scheduler.run()

if __name__ == '__main__':
    #项目入口
    main()
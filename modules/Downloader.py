# -*- coding: utf-8 -*-
'''
@author: tieqiang Xu
@mail: 805349916@qq.com
'''
import threading

from modules.Parser import Parser
from utils.HttpUtils import HttpUtils
from utils.InitUtils import InitUtils
from utils.LogUtils import log


class Downloader():
    '''
    下载器，访问http/ftp/ssh等
    1.获取response
    2.下载文件
    '''
    def __init__(self,task):
        threading.Thread.__init__(self)
        self.task=task

    def run(self):
        '''
        线程执行，默认调用方法，任务分发
        :return:
        '''
        log.i ('Downloader.run()')
        if self.task['parser'] in ['demo']:
            self.get_default_html()
        else:
            self.get_default_html()
        parser=Parser(self.task)
        parser.run()

    def get_default_html(self):
        proxies = {
            "http": "http://"+HttpUtils.get_proxy()
        }
        proxies = None  #不使用代理服务器
        headers = {
            "User-Agent": HttpUtils.get_useragent()
        }
        cookies = None #不使用cookie
        r = HttpUtils.get_html(self.task['request'], headers=headers, proxies=proxies, cookies=cookies)
        self.task['response'] = r
        #log.d(self.task)

if __name__ == '__main__':
    initUtils=InitUtils()
    initUtils.init()
    task={
        "_id":"1",
        "state": "doing",
        "parser":"demo",
        "request":"http://www.baidu.com",
        "parent":{}
    }
    d=Downloader(task)
    d.run();
    pass
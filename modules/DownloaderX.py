# -*- coding: utf-8 -*-
'''
@author: tieqiang Xu
@mail: 805349916@qq.com
'''
import threading

from modules.ParserX import ParserX
from utils.HttpUtil import HttpUtil
from utils.InitUtil import InitUtil
from utils.LogUtil import Log


class DownloaderX():
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
        Log.i ('Downloader.run()')
        if self.task['parser'] in ['demo']:
            self.get_default_html()
        else:
            self.get_default_html()
        parserX=ParserX(self.task)
        parserX.run()

    def get_default_html(self):
        proxies = {
            "http": "http://"+HttpUtil.get_proxy()
        }
        proxies = None  #不使用代理服务器
        headers = {
            "User-Agent": HttpUtil.get_useragent()
        }
        cookies = None #不使用cookie
        r = HttpUtil.get_html(self.task['request'], headers=headers, proxies=proxies, cookies=cookies)
        self.task['response'] = r
        #log.d(self.task)

if __name__ == '__main__':
    initUtil=InitUtil()
    initUtil.init()
    task={
        "_id":"1",
        "state": "doing",
        "parser":"demo",
        "request":"http://www.baidu.com",
        "parent":{}
    }
    d=DownloaderX(task)
    d.run();
    pass
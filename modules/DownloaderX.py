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
        #利用反射机制自动执行download_<parser名>（）函数，如果找不到则执行默认的download_default()函数
        if hasattr(self, 'download_'+self.task['parser']):
            func = getattr(self, 'download_'+self.task['parser'])
            func()
        else:
            self.download_default()
        parserX=ParserX(self.task)
        parserX.run()

    def download_default(self):
        proxies = {
            "http": "http://"+HttpUtil.get_proxy()
        }
        proxies = None  #不使用代理服务器
        headers = {
            "User-Agent": HttpUtil.get_useragent()
        }
        cookies = None #不使用cookie
        r=None
        if(self.task['request'].startswith('https://')):
            r = HttpUtil.gets_html(self.task['request'], headers=headers, proxies=proxies, cookies=cookies)
        else:
            r = HttpUtil.get_html(self.task['request'], headers=headers, proxies=proxies, cookies=cookies)
        self.task['response'] = r

if __name__ == '__main__':
    initUtil=InitUtil()
    initUtil.init()
    task={
        "_id":"1",
        "state": "doing",
        "table": "demo_info",
        "parser":"demo",
        "request":"http://www.baidu.com",
        "parent":{}
    }
    d=DownloaderX(task)
    d.run();
    pass
# -*- coding: utf-8 -*-
'''
@author: tieqiang Xu
@mail: 805349916@qq.com
'''
import importlib
import threading

from configs import Setting
from utils.HttpUtil import HttpUtil
from utils.InitUtil import InitUtil
from utils.LogUtil import Log


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
        Log.i ('Downloader.run()')
        #利用反射机制自动执行download_<parser名>（）函数，如果找不到则执行默认的download_default()函数
        if hasattr(self, 'download_'+self.task['parser']):
            func = getattr(self, 'download_'+self.task['parser'])
            func()
        else:
            self.download_default()
        #启动解析器
        parserModule = Setting.PARSER_MODULE
        ParserX = importlib.import_module(parserModule)
        parser = ParserX.Parser(self.task)
        parser.run()

    def download_default(self):
        #配置代理服务器
        proxies = None  #不使用代理服务器
        if Setting.HTTP_PROXY is not None:
            proxies = {
                "http": "http://"+Setting.HTTP_PROXY
            }
        #配置Http header（User-Agent）
        headers = None #不自定义header
        if Setting.USER_AGENT is not None:
            headers = {
                "User-Agent": Setting.USER_AGENT
            }
        #配置referer
        if Setting.REFERER is not None:
            if headers is None:
                headers = {
                    "Referer": Setting.REFERER
                }
            else:
                headers['Referer'] = Setting.REFERER
        #配置cookies
        if Setting.COOKIES is not None:
            if headers is None:
                headers = {
                    "Cookie": Setting.COOKIES
                }
            else:
                headers['Cookie'] = Setting.COOKIES
        #请求HTTP
        r=None
        if(self.task['request'].startswith('https://')):
            r = HttpUtil.gets_html(self.task['request'], headers=headers, proxies=proxies, cookies=None)
        else:
            r = HttpUtil.get_html(self.task['request'], headers=headers, proxies=proxies, cookies=None)
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
    d=Downloader(task)
    d.run();
    pass
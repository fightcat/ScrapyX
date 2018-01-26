# coding:utf-8
'''
访问http
1.获取response
2.下载文件
'''
import threading
from utils.HttpUtils import HttpUtils
from Parser import Parser

class Downloader():

    def __init__(self,task):
        threading.Thread.__init__(self)
        self.task=task

    def run(self):
        '''
        线程执行，默认调用方法，任务分发
        :return:
        '''
        print ('Downloader.run()')
        if self.task['parser'] in ['demo']:
            self.get_default_html()
        else:
            self.get_default_html()
        parser=Parser(self.task)
        parser.run()

    def get_default_html(self):
        proxies = {
            "http": "http://127.0.0.1:8888"
        }
        proxies = None
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"
        }
        r = HttpUtils.get_html(self.task['request'], headers=headers, proxies=proxies)
        self.task['response'] = r
        print (self.task)

if __name__ == '__main__':
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
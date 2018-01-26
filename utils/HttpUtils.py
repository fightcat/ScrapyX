# coding:utf-8
'''
访问http
1.获取response
2.下载文件
'''
import requests

class HttpUtils:

    def __init__(self):
        pass

    @staticmethod
    def get_header(url, params=None, headers=None, cookies=None, proxies=None):
        '''
        发送http head请求
        :param url:str 请求的url
        :return: dict header值
        '''
        r = requests.get(url)
        return r.headers

    @staticmethod
    def get_html(url, params=None, headers=None, cookies=None, proxies=None, charset='UTF-8'):
        '''
        发送http get请求
        :param url:str 请求的url
        :param params:dict 参数
        :param headers:dict 自定义请求头
        :param cookies:dict 网站cookies
        :param proxies:dict 代理
        :return: str 返回的str文本
        '''
        r = requests.get(url, params=params, headers=headers, cookies=cookies, proxies=proxies)
        r.encoding = charset
        return r.text

    @staticmethod
    def get_json(url, params=None, headers=None, cookies=None, proxies=None, charset='UTF-8'):
        '''
        发送http get请求
        :param url:str 请求的url
        :param params:dict 参数
        :param headers:dict 自定义请求头
        :param cookies:dict 网站cookies
        :param proxies:dict 代理
        :return: json 返回的json对象
        '''
        r = requests.get(url, params=params, headers=headers, cookies=cookies, proxies=proxies)
        r.encoding = charset
        return r.json()

    @staticmethod
    def get_file(file_name, url, params=None, headers=None, cookies=None, proxies=None):
        '''
        发送http get请求文件
        :return:
        '''
        r = requests.get(url, params=params, headers=headers, cookies=cookies, proxies=proxies)
        with open(file_name, 'wb') as fd:
            for chunk in r.iter_content(512):
                fd.write(chunk)
        return

    @staticmethod
    def post_html(url, data=None, headers=None, cookies=None, proxies=None, charset='UTF-8'):
        '''
        发送http post请求
        :param url:str 请求的url
        :param data:dict post的数据
        :param headers:dict 自定义请求头
        :return: str 返回的str文本
        '''
        r = requests.post(url, data=data, headers=headers, cookies=cookies, proxies=proxies)
        r.encoding = charset
        return r.text

    @staticmethod
    def gets_html(url, params=None, headers=None, cookies=None, proxies=None, charset='UTF-8'):
        '''
        发送https get请求
        :param url:str 请求的url
        :param params:dict 参数
        :param headers:dict 自定义请求头
        :param cookies:dict 网站cookies
        :param proxies:dict 代理
        :return: str 返回的str文本
        '''
        r = requests.get(url, params=params, headers=headers, cookies=cookies, proxies=proxies, verify=False)
        r.encoding = charset
        return r.text

    @staticmethod
    def posts_html(url, data=None, headers=None, cookies=None, proxies=None, charset='UTF-8'):
        '''
        发送https post请求
        :param url:str 请求的url
        :param data:dict post的数据
        :param headers:dict 自定义请求头
        :return: str 返回的str文本
        '''
        r = requests.post(url, data=data, headers=headers, cookies=cookies, proxies=proxies, verify=False)
        r.encoding = charset
        return r.text



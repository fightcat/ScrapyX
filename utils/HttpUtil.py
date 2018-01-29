# -*- coding: utf-8 -*-
'''
@author: tieqiang Xu
@mail: 805349916@qq.com
'''
import requests

from utils.LogUtils import log

class HttpUtil:
    '''
    访问http/https
    1.获取response
    2.下载文件
    '''
    def __init__(self):
        pass

    @staticmethod
    def get_header(url, params=None, headers=None, cookies=None, proxies=None):
        '''
        发送http head请求
        :param url:str 请求的url
        :return: dict header值
        '''
        html = None
        try:
            r = requests.get(url)
            html=r.headers
        except Exception as e:
            log.e("http get header failed -> " + str(e))
        finally:
            pass
        return html

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
        html = None
        try:
            r = requests.get(url, params=params, headers=headers, cookies=cookies, proxies=proxies)
            r.encoding = charset
            html=r.text
        except Exception as e:
            log.e("http get html failed -> " + str(e))
        finally:
            pass
        return html

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
        html = None
        try:
            r = requests.get(url, params=params, headers=headers, cookies=cookies, proxies=proxies)
            r.encoding = charset
            html = r.json()
        except Exception as e:
            log.e("http get json failed -> " + str(e))
        finally:
            pass
        return html

    @staticmethod
    def get_file(file_name, url, params=None, headers=None, cookies=None, proxies=None):
        '''
        发送http get请求文件
        :return:
        '''
        html = True
        try:
            r = requests.get(url, params=params, headers=headers, cookies=cookies, proxies=proxies)
            with open(file_name, 'wb') as fd:
                for chunk in r.iter_content(512):
                    fd.write(chunk)
        except Exception as e:
            log.e("http get file failed -> " + str(e))
            html=False
        finally:
            pass
        return html

    @staticmethod
    def post_html(url, data=None, headers=None, cookies=None, proxies=None, charset='UTF-8'):
        '''
        发送http post请求
        :param url:str 请求的url
        :param data:dict post的数据
        :param headers:dict 自定义请求头
        :return: str 返回的str文本
        '''
        html = None
        try:
            r = requests.post(url, data=data, headers=headers, cookies=cookies, proxies=proxies)
            r.encoding = charset
            html = r.text
        except Exception as e:
            log.e("http post html failed -> " + str(e))
        finally:
            pass
        return html

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
        html = None
        try:
            r = requests.get(url, params=params, headers=headers, cookies=cookies, proxies=proxies, verify=False)
            r.encoding = charset
            html = r.text
        except Exception as e:
            log.e("https get html failed -> " + str(e))
        finally:
            pass
        return html

    @staticmethod
    def posts_html(url, data=None, headers=None, cookies=None, proxies=None, charset='UTF-8'):
        '''
        发送https post请求
        :param url:str 请求的url
        :param data:dict post的数据
        :param headers:dict 自定义请求头
        :return: str 返回的str文本
        '''
        html=None
        try:
            r = requests.post(url, data=data, headers=headers, cookies=cookies, proxies=proxies, verify=False)
            r.encoding = charset
            html=r.text
        except Exception as e:
            log.e("https post html failed -> " + str(e))
        finally:
            pass
        return html

    @staticmethod
    def get_useragent():
        '''
        获取useragent
        :return: string
        '''
        return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'

    @staticmethod
    def get_proxy():
        '''
        获取代理服务器地址及端口，格式ip:port
        :return: string
        '''
        return '127.0.0.1:8888'

    @staticmethod
    def get_cookie():
        '''
        获取cookie
        :return:
        '''
        return ''

if __name__ == '__main__':
    r=HttpUtil.get_html(url="http://www.736372726382863.com")
    print(r)
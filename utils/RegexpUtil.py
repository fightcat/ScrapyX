#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: tieqiang Xu
# @Email: 805349916@qq.com
# @Time: 2018/1/29 0029
import re

class RegexpUtil():
    '''
    正则表达式工具类
    '''
    @staticmethod
    def subs(source,regexp):
        '''
        返回source中regexp匹配的group部分,列表形式
        :param source: string，源串
        :param regexp: string，正则表达式串
        :return: string 返回中间部分字符串列表
        '''
        m = re.findall(regexp, source)
        return m

    @staticmethod
    def sub(source,regexp):
        '''
        返回source中regexp匹配的group部分,第1个字符串
        :param source: string，源串
        :param regexp: string，正则表达式串
        :return: string 返回中间部分字符串
        '''
        result = None
        m = re.findall(regexp, source)
        if m is not None and len(m) >= 1:
            result = m[0]
        return result

    @staticmethod
    def substrings(source,start_string,end_string):
        '''
        返回source中start_string与end_string之间的部分,列表形式
        注意start_string与end_string中的符号要用\转义
        :param source: string，源串
        :param start_string: string，起始串
        :param end_string: string，结束串
        :return: string 返回中间部分字符串列表
        '''
        m = re.findall(start_string+"(.+?)"+end_string, source)
        return m

    @staticmethod
    def substring(source,start_string,end_string):
        '''
        返回source中start_string与end_string之间的部分,第1个字符串
        注意start_string与end_string中的符号要用\转义
        :param source: string，源串
        :param start_string: string，起始串
        :param end_string: string，结束串
        :return: string 返回中间部分字符串
        '''
        result=None
        m = re.findall(start_string + "(.+?)" + end_string, source)
        if m is not None and len(m)>=1:
            result=m[0]
        return result

    @staticmethod
    def replaces(source,regexp,newvalue,count=0):
        '''
        从source中按regexp匹配查找串，替换成newvalue
        :param source: 源串
        :param regexp: 匹配的regexp规则
        :param newvalue: 匹配到的部分替换成的新串
        :param count: 替换次数，0代表全部替换
        :return: 替换之后的完整新串
        '''
        dest, number = re.subn('resize_(\d)+x(\d)+', 'image_resize', source, count)
        return dest

    @staticmethod
    def replace(source,regexp,newvalue):
        '''
        从source中按regexp匹配查找串，替换成newvalue，只替换第1个
        :param source: 源串
        :param regexp: 匹配的regexp规则
        :param newvalue: 匹配到的部分替换成的新串
        :return: 替换之后的完整新串
        '''
        dest, number = re.subn('resize_(\d)+x(\d)+', 'image_resize', source, count=1)
        return dest

    @staticmethod
    def getNumbers(source):
        '''
        用正则表达式，获取字符串中的所有数字，列表形式
        :param source: 源串
        :return: list<string> 数字列表
        '''
        m = re.findall(r'\d+', source)  # 获取所有数字
        return m

    @staticmethod
    def getNumber(source,default=None):
        '''
        用正则表达式，获取字符串中的第1组数字
        :param source: 源串
        :return: string 数字
        '''
        result=default
        m = re.findall(r'\d+', source)  # 获取所有数字
        if m is not None and len(m) >= 1:
            result=m[0]
        return m
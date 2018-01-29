# -*- coding: utf-8 -*-
'''
@author: tieqiang Xu
@mail: 805349916@qq.com
'''
import configparser
import os

config = configparser.ConfigParser()
conf_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..','configs','config.ini')
config.read(conf_file,encoding='UTF-8')

class ConfigUtil(object):
    '''
    读取ini配置文件
        ini文件结构如下：
        [Section1]
        option1 : value1
        option2 : value2
    '''

    def __init__(self):
        pass

    @staticmethod
    def getItems(section):
        '''
        获取section下所有kv对
        :param section: section名
        :return:
        '''
        return config._sections[section]

    @staticmethod
    def get(section,option):
        '''
        获取section下option对应的值
        :param section: section名
        :param option: option名
        :return:object
        '''
        return config.get(section,option)

    @staticmethod
    def getInt(section,option):
        '''
        获取section下option对应的int值
        :param section:
        :param option:
        :return:int
        '''
        return config.getint(section,option)

    @staticmethod
    def getBoolean(section,option):
        '''
        获取section下option对应的boolean值
        :param section:
        :param option:
        :return:int
        '''
        return config.getboolean(section,option)

    @staticmethod
    def getFloat(section, option):
        '''
        获取section下option对应的float值
        :param section:
        :param option:
        :return:int
        '''
        return config.getfloat(section, option)

if __name__ == '__main__':
    items=ConfigUtil.getItems('scheduler')
    print (items)
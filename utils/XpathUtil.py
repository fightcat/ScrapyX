#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: tieqiang Xu
# @Email: 805349916@qq.com
# @Time: 2018/1/29 0029

from lxml import etree

class XpathUtil():
    '''
    Xpath工具类
    '''
    @staticmethod
    def getRoot(html):
        '''
        获取html的根结点对象
        :param html: string，html文档
        :return: _Element，根结点对象
        '''
        return etree.HTML(html)

    @staticmethod
    def getNodes(node,xpath):
        '''
        从node中匹配xpath，返回节点列表
        :param node: _Element，待匹配的父节点
        :param xpath: string，xpath路径
        :return: list<_Elemnet>，匹配到的节点列表
        '''
        return node.xpath(xpath)

    @staticmethod
    def getNode(node,xpath):
        '''
        从node中匹配xpath，返回第1个节点对象
        :param node: _Element，待匹配的父节点
        :param xpath: string，xpath路径
        :return: _Element，匹配到的节点
        '''
        nodes=node.xpath(xpath)
        if nodes is not None and len(nodes)>=1:
            return nodes[0]
        else:
            return None

    @staticmethod
    def getAttribs(node, xpath):
        '''
        从nodex中匹配xpath，返回属性列表
        注意xpath应以“/@属性名”结尾
        :param node: _Element，待匹配的父节点
        :param xpath: string，xpath路径
        :return: list<_ElementUnicodeResult>，匹配到的属性值列表
        '''
        return node.xpath(xpath)



    @staticmethod
    def getAttrib(node, xpath, trim=True, default=None):
        '''
        从node中匹配xpath，返回第1个属性值
        :param node: _Element，待匹配的父节点
        :param xpath: string，xpath路径
        :param trim: bool，是否转义&nbsp，并去掉前后空格
        :param default: string，取不到时的默认值
        :return: string，匹配到的属性值
        '''
        result=None
        attrs = node.xpath(xpath)
        if attrs is not None and len(attrs) >= 1:
            if trim:
                result=XpathUtil.htmltrim(str(attrs[0]))
            else:
                result=str(attrs[0])
        if result is None:
            result=default;
        return result

    @staticmethod
    def getNodeAttrib(node, attrib, trim=True, default=None):
        '''
        获取节点的指定属性值
        :param node: _Element，待获取的源节点
        :param attrib: string，属性名
        :param trim: bool，是否转义&nbsp，并去掉前后空格
        :return: string，属性值，转义&nbsp，并去掉了前后空格
        '''
        result=None
        if attrib in node.attrib:
            if trim:
                result = XpathUtil.htmltrim(str(node.attrib[attrib]))
            else:
                result = str(node.attrib[attrib])
        if result is None:
            result=default;
        return result

    @staticmethod
    def getTexts(node, xpath):
        '''
        从node中匹配xpath，返回innerText文本信息列表
        注意xpath应以“/text()”结尾
        :param node: _Element，待匹配的父节点
        :param xpath: string，xpath路径
        :return: list<_ElementUnicodeResult>，匹配到的innerText文本信息列表
        '''
        return node.xpath(xpath)

    @staticmethod
    def getText(node, xpath, trim=True, default=None):
        '''
        从node中匹配xpath，返回第1个innerText文本信息
        :param node: _Element，待匹配的父节点
        :param xpath: string，xpath路径
        :param trim: bool，是否转义&nbsp，并去掉前后空格
        :return: string，匹配到的innerText文本信息
        '''
        result = None
        texts = node.xpath(xpath)
        if texts is not None and len(texts) >= 1:
            if trim:
                result = XpathUtil.htmltrim(str(texts[0]))
            else:
                result = str(texts[0])
        if result is None:
            result=default;
        return result

    @staticmethod
    def htmltrim(str):
        '''
        对str源字符串替换&nbsp为正常空格，并去掉首尾空格
        :param str:
        :return:
        '''
        return str.replace('\xc2\xa0', ' ').strip()

if __name__ == '__main__':
    html='<div><p class="nav">导航123GO</p><p>  空&nbsp;格&nbsp;    </p></div>'
    root=XpathUtil.getRoot(html)
    nodes=XpathUtil.getNodes(root,'//div/p')
    node=XpathUtil.getNode(root,'//div/p')
    attribs=XpathUtil.getAttribs(root,'//div/p/@class')
    attrib=XpathUtil.getAttrib(root,'//div/p/@class')
    attrib=XpathUtil.getNodeAttrib(root,'class')
    innerText = XpathUtil.getText(root, '//div/p/text()')
    print(innerText)
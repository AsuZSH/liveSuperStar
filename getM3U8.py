#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 因为存在JavaScript动态加载，需要 PhantomJS：https://phantomjs.org/download.html
from ast import If
import time  # 使用延时
import csv  # 进行 .CSV 文件读写
from sys import argv
import re  # 字符串正则
from selenium import webdriver  # 动态网页获取 pip install selenium==2.48.0
from urllib.parse import unquote  # 导入urlencode库，之后对url解码

# example:python3 cmd.py http://www.jiaxingren.com/folder24/folder147/folder149/folder170/2018-10-25/416269.html
# websiteUrl = "http://newesxidian.chaoxing.com/live/viewNewCourseLive1?isStudent=1&liveId=11016166" # 问题URL
# websiteUrl = "http://newesxidian.chaoxing.com/live/viewNewCourseLive1?isStudent=1&liveId=11017158"  # 正常URL
# if len(argv) < 2:
#     exit('请输入网页地址')
# else:
#     websiteUrl = argv[1]

# if websiteUrl == '':
#     exit('请输入网页地址')


class getM3U8:
    def getM3U8(websiteUrl):
        # 抓取 m3u8
        browser = webdriver.PhantomJS()
        browser.get(websiteUrl)

        # # 强制等待30秒，超星加载wrnmd
        # time.sleep(30)

        # 间隔3s，请求m3u8数据，直到成功
        m3u8_info_temp = browser.find_element_by_xpath(
            '//*[@id="viewFrame"]').get_attribute("src")
        while len(m3u8_info_temp) < 100:
            time.sleep(3)
            m3u8_info_temp = browser.find_element_by_xpath(
                '//*[@id="viewFrame"]').get_attribute("src")
        HTML_info_temp = browser.page_source
        browser.close()

        # 处理 m3u8 数据，最终输出到 m3u8_mobile
        # 对请求到的m3u8数据，进行urlcode解码
        m3u8_info = unquote(m3u8_info_temp)
        HTML_info = unquote(HTML_info_temp)

        # 检索文字设定：m3u8_info_mobile_temp
        m3u8_info_mobile_temp = re.compile(
            r'((https|http|ftp|rtsp|mms)[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+m3u8\b)', re.S)  # 正则匹配

        # 检索结果，输出列表：m3u8_mobile_temp
        m3u8_mobile_temp = re.findall(m3u8_info_mobile_temp, m3u8_info)

        # 检索结果处理
        # 根据最终 待选 m3u8 数量是否 >=2 判断其有效性
        if len(m3u8_mobile_temp) >= 2:
            m3u8_mobile = str(m3u8_mobile_temp[1])[2:-10]
            print(m3u8_mobile)
            print()
            # 返回 m3u8
            return m3u8_mobile
        else:
            print('问题URL(请查看AllErrorURL.csv): ', websiteUrl)
            return "null"

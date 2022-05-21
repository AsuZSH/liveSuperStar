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


class getM3U8_info:
    def getM3U8_info(websiteUrl):
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

        # 关于m3u8信息回传
        return m3u8_info

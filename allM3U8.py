#!/usr/bin/env python
# coding: utf-8

# In[31]:


# -*- coding: UTF-8 -*-
# 因为存在JavaScript动态加载，需要 PhantomJS：https://phantomjs.org/download.html
import time  # 使用延时
from sys import argv
import re  # 字符串正则
import csv  # 进行 .CSV 文件读写
from selenium import webdriver  # 动态网页获取 pip install selenium==2.48.0
from getM3U8 import getM3U8  # 调用getM3U8

# example:python3 cmd.py http://www.jiaxingren.###
if len(argv) < 2:
    exit('请输入网页地址')
else:
    websiteUrl = argv[1]

if websiteUrl == '':
    exit('请输入网页地址')

# 抓取 直播ID
browser = webdriver.PhantomJS()
browser.get(websiteUrl)


i = 1

# time.sleep(10)
# live_id_info_list随便赋个空，等它改变
live_id_info_list = []
while live_id_info_list == []:
    try:
        # 不能确定是否正确执行的代码
        live_id_info_list = browser.find_elements_by_xpath(
            '//*[@class="w_tab_btn w_live_btn"]')
    except:
        time.sleep(2)
# 将 直播id 数量存到num_id
num_id = len(live_id_info_list)
print('获取视频列表成功，数量：' + str(num_id))
# 提示
print('网页加载需要较长时间，请等待(一般30秒之内)。。。')
print('请不要在程序运行时打开 .csv 文件')


# for循环，循环处理各视频
for i in range(1, num_id+1):
    # 输出当前序号
    print('当前处理：第' + str(i) + '/' + str(num_id) + '个视频')
    # 制作live_info_xpath
    live_info_xpath = '//*[@id="signleCourseList"]/li[' + str(i) + ']/div/a'
    # 获取 id 对应信息live_info_temp
    live_info_temp = browser.find_element_by_xpath(
        live_info_xpath).get_attribute("href")

    # name 直接可用
    # 制作name_xpath
    name_xpath = '//*[@id="signleCourseList"]/li[' + str(i) + ']/p'
    # 获取 name 对应信息name
    name = browser.find_element_by_xpath(
        name_xpath).get_attribute("textContent")
    name = name.replace(" ", "")
    HTML_info_temp = browser.page_source

    # 检索文字设定：live_info_inse
    live_info_inse = re.compile(
        r'([1-9][0-9]{4,})', re.S)  # 正则匹配

    # 检索结果，输出列表：live_temp
    live_temp = re.findall(live_info_inse, live_info_temp)

    # 检索结果处理
    live_id = str(live_temp[0])

    # 获得M3U8
    # 检索文字设定：URL_inse
    URL_inse = re.compile(
        r'[a-zA-z]+://[^\s]*liveId=\b', re.S)  # 正则匹配
    # 检索结果，输出URL前缀列表：URL_temp
    URL_temp = re.findall(URL_inse, websiteUrl)
    # 拼接URL前缀 id
    websiteUrl = str(URL_temp)[2:-2] + live_id
    m3u8 = getM3U8.getM3U8(websiteUrl)

    # print(name)
    # print()
    # print(m3u8)

    # 写入 .csv
    # 文件名，保存位置，m3u8 正常数据写入Allm3u8.csv
    if m3u8 != 'null':
        with open('Allm3u8.csv', 'a', newline='') as file:
            Allm3u8TempWriter = csv.writer(file)
            Allm3u8TempWriter.writerow(
                [name, "%USERPROFILE%\Videos\M3U8", m3u8])
    # 时间，文件名，m3u8 错误数据写入 AllErrorURL.csv
    else:
        with open('AllErrorURL.csv', 'a', newline='') as AllErrorGet:
            ErrorURLWriter = csv.writer(AllErrorGet)
            ErrorURLWriter.writerow(
                [str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))), name, websiteUrl])
# 任务结束，关闭浏览器
browser.close()
print()
print('任务结束！')

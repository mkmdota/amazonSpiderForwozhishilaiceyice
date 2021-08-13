#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2021/8/9 0:31
# @Author: Bolvar Fordragon
# @File  : v0.py
# 放一些固定不改的函数


import os
import time
import json
from selenium import webdriver


def preparation():
    # 前期准备，记录开始时间，创建工作目录
    start_time = time.strftime('%Y-%m-%d %H{}%M{}%S', time.localtime(time.time())).format('：', '：')
    print('开始时间：%s' % start_time)
    # 生成年月日时
    directory_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    print('时间路径:%s' % directory_time)
    # 生成年月日时分秒
    # item_time = time.strftime('%Y-%m-%d %H{}%M{}%S', time.localtime(time.time())).format('：', '：')
    # print(item_time)
    # 生成文件目录
    File_Path = os.getcwd() + '\\' + directory_time + '\\'
    print('文件路径:%s' % File_Path)
    File_Path_product_principal_screenshot = '%s\\product_principal_screenshot\\' % File_Path
    File_Path_product_details = '%s\\product details\\' % File_Path
    File_Path_reviews = '%s\\reviews\\' % File_Path
    print('主体路径:%s' % File_Path_product_principal_screenshot)
    print('详情路径:%s' % File_Path_product_details)
    print('评论路径:%s' % File_Path_reviews)
    # 获取到当前文件的目录，并检查是否有 所需要的 文件夹，如果不存在则自动新建 所需要的 文件夹
    for p in [File_Path, File_Path_product_principal_screenshot, File_Path_product_details, File_Path_reviews]:
        try:
            if not os.path.exists(p):
                os.makedirs(p)
                print("目录创建成功：%s" % p)
            else:
                print("目录已存在：%s" % p)
        except Exception as msg:
            print("目录创建失败：%s【%s】" % (p, msg))
    return start_time, File_Path, File_Path_product_principal_screenshot, File_Path_product_details, File_Path_reviews


def loadDataFromJson():
    data = json.load(open("asin.json", "r"))
    # json: {key1:[asin1, asin2...], key2:[asin1, asin2...], ...}
    asin_list = []
    for k, v in data.items():
        asin_list.extend(v)
    asin_list = list(set(asin_list))
    print("获取ASIN数量：%s" % len(asin_list))
    return asin_list


def equal_distribution_list(target_list, list_n):
    list_o = target_list.copy()  # origin
    data_len = len(list_o)
    list_t = []  # target
    for temp in range(list_n):
        list_t.append([])
    #print(len(list_o))
    for tempx in range(data_len // list_n):
        for tempy in range(list_n):
            list_t[tempy].append(list_o.pop())
    #print(len(list_o))
    for temp in range(data_len % list_n):
        list_t[temp].append(list_o.pop())
    #print(len(list_o))
    print(len(list_t), [len(i) for i in list_t])
    return list_t


def seleniumTest(testurl='http://www.baidu.com', drivers='All'):
    driverpass = []
    if drivers == 'Edge':
        try:
            browser_e = webdriver.Edge('D:/WebDriver/bin/MicrosoftWebDriver.exe')
            browser_e.get(testurl)
            browser_e.quit()
            driverpass.append('Edge')
        except Exception as e:
            print('Edge error', e)
    elif drivers == 'Chrome':
        try:
            browser_c = webdriver.Chrome('D:/WebDriver/bin/chromedriver.exe')
            browser_c.get(testurl)
            browser_c.quit()
            driverpass.append('Chrome')
        except Exception as e:
            print('Chrome error', e)
    elif drivers == 'Firefox':
        try:
            browser_f = webdriver.Firefox()
            browser_f.get(testurl)
            browser_f.quit()
            driverpass.append('Firefox')
        except Exception as e:
            print('Firefox error', e)
    else:
        list_temp = []
        for d in ['Edge', 'Chrome', 'Firefox']:
            list_temp.extend(seleniumTest(testurl=testurl, drivers=d))
        return list_temp
    return driverpass


def getallfiles(filepath, filetype=None):
    pathDir = os.listdir(filepath)
    allfiles = []
    for allDir in pathDir:
        child = os.path.join(filepath, allDir)
        if filetype != None:
            if type(filetype) == str:
                if child.endswith(filetype):
                    allfiles.append(child)
            else:
                print('File Type Error Return All Files')
                allfiles.append(child)
        else:
            allfiles.append(child)
    return allfiles


if __name__ == '__main__':
    print(seleniumTest())

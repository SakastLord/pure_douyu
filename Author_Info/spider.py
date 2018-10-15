#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Lix'

# from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.common.by import By
import time
#import re
import requests
import os


class driveSpider:
    def __init__(self,url):
        """初始化构造函数
        """
        self.site_url = url
        self.driver = webdriver.Chrome(executable_path='chromedriver.exe')
        self.sleep_time = 3



    def getItem(self):
        for i in range(100):
            try:
                self.driver.get(self.site_url)
                break
            except Exception as e:
                print(e)

        time.sleep(self.sleep_time)
        html = self.driver.page_source.encode('utf-8')
        selector = etree.HTML(html)

        try:
            fans_list = selector.xpath('//*[@id="mCSB_3_container"]/ul')
            for fan in fans_list:
                fan = fan['li']
                print(fan)
        except:
            print('粉丝收集失败')



        try:
            paiming = selector.xpath("//*[@id=\"anchor-info\"]/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/span/span")[0].text
        except:
            paiming=''
            print('排名收集失败')
        try:
            guanzhu = selector.xpath("//*[@id=\"anchor-info\"]/div[3]/div[1]/div[2]/p/span")
            if len(guanzhu)==0:
                guanzhu = selector.xpath("//*[@id=\"anchor-info\"]/div[4]/div[1]/div[2]/p/span")[0].text
            else:
                guanzhu=guanzhu[0].text
        except:
            guanzhu=''
            print('关注量获取失败')

        try:
            jingyan = selector.xpath('//*[@id="js-anchor-level-wrap"]/div/div/div[1]/a[1]')[0].text.replace('\n','').replace(' ','')+','+selector.xpath('//*[@id="js-anchor-level-wrap"]/div/div/div[1]/a[2]/span')[0].text.replace('\n','').replace(' ','')
        except:
            print('经验值捕获异常')
            jingyan = ''

        try:
            dianfeng = selector.xpath('//*[@id="anchor-info"]/div[2]/div[2]/div[2]/a/span[2]')[0].text
        except:
            dianfeng =''
            print('巅峰值缺失')

        try:
            shuiyou = selector.xpath('//*[@id="groupListBox"]/div[1]/a')[0].text.split("个水友正在鱼吧讨论, 去看看 & gt; & gt; ")[0]
        except:
            shuiyou =''
            print('水友收集失败')
        try:
            main_url = selector.xpath("//*[@id=\"anchor-info\"]/div[3]/div[1]/span/a/@href")

            if len(main_url)==0:
                main_url = selector.xpath("//*[@id=\"anchor-info\"]/div[4]/div[1]/span/a/@href")[0]
            else:
                main_url = main_url[0]
        except:
            main_url = ''
            print('主页收集失败')
        hashname = main_url[27:]
        f = open('zhubo_home.txt', 'a')
        f.write(main_url + '\n')
        f.close()
        for i in range(100):
            try:
                self.driver.get(main_url)
                break
            except Exception as e:
                print(e)
        html = self.driver.page_source.encode('utf-8')
        selector = etree.HTML(html)

        time.sleep(self.sleep_time)

        try:
            shipin_num = selector.xpath('//*[@id="container"]/div[1]/div[1]/div[2]/ul/li[1]/div/p[1]')[0].text
        except:
            # shipin_num = selector.xpath('//*[@id="container"]/div[1]/div[1]/div[2]/ul/li[1]/div/p[1]')
            shipin_num=''
            print('错误')
        try:
         bofang_num = selector.xpath('//*[@id="container"]/div[1]/div[1]/div[2]/ul/li[2]/div/p[1]')[0].text
        except:
            bofang_num=''
            print('错误')
        self.driver.quit()
        return paiming, guanzhu, shipin_num, bofang_num,shuiyou,jingyan,dianfeng,hashname

    def run(self):
        self.getItem()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'sunjifeng'

import math
import csv
import requests

class shipinInfo:
    def __init__(self):
        """初始化构造函数
        """
        self.url_list = []
        self.site_host='https://v.douyu.com/video/author/getAuthorVideoListByNew?up_id='
        self.video_numlist=[]

    def getUrl(self):
        """获取页面代码
        """
        with open('Author_Info/zhubo_home.txt') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip('\n')
                self.url_list.append(line[27:])


    def getPage(self,url):
        try:
            page= requests.get(self.site_host+url).json()['data']
            video_num = page['count']
            print(video_num)

            if video_num <= 120:
                video_list = page['list']
                for video in video_list:
                    f = open('shipin_info.csv','a', newline="", encoding="utf-8")
                    v = csv.writer(f)
                    v.writerow([url,video['create_time'],video['update_time'],video['view_num'],video['video_duration'],video['hash_id']])
                    f.close()
                    print(video['view_num'])
            else:
                print(url+'多于一页')
                video_list=[]
                for i in range(math.ceil(video_num/120)):
                    p= i+1
                    video_list.append(requests.get(self.site_host+url+'&page='+str(p)).json()['data']['list'])
                    print('当前第'+str(p)+'页')
        except Exception as err:
            print(err)


def main():
    dy = shipinInfo()
    dy.getUrl()
    print(dy.url_list)
    for url in dy.url_list:
        dy.getPage(url)


if __name__ == "__main__":
    main()
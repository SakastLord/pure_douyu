#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'sunjifeng'
'''
关于代码的说明：
单独运行的代码块用目录加以区分，不同的代码块之间有关联的只会在读取的文本文件上
Author_Info文件夹获取的信息为主播信息，
'类別','主播', '链接', '人氣指數', '房间id','周排名', '关注数目',
'视频数目','播放总量', '水友数目'
写入zhubo_info.csv文件中
'''
import requests
from bs4 import BeautifulSoup
import time, datetime
import csv
from Author_Info.spider import driveSpider
class douyu_host_info():
    def __init__(self):
        self.url_host = 'https://www.douyu.com'
        self.date_time = datetime.datetime.now().strftime('%Y%m%d_%H%M')
        #self.driver = webdriver.Chrome(executable_path='chromedriver.exe')
        #self.sleep_time=1
        self.url_list = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        }

        self.old_categorys_list = [
             '/g_jdqs','/g_TVgame', '/g_classic', '/g_gwlrsj', '/g_FTG', '/g_xyqx', '/g_BF','/g_NBA2K','/g_famine','/g_DECEIT','/g_lhcm','/g_qmzz','/g_AC','/g_qmyks','/g_RUST','/g_xpkz',
            '/g_RR', '/g_fs', '/g_Scum','/g_gjsd','/g_dzzh','/g_sljt','/g_jxjs','/g_gmly','/g_ryzh','/g_SGZ','/g_COD','/g_twhj','/g_dstjx','/g_hyrzjjfbs','/g_jpfc','/g_ozkcmn','/g_ztsj'
        ]

        self.categorys_list = [
            '/g_jdqs', '/g_TVgame', '/g_classic', '/g_gwlrsj', '/g_FTG', '/g_xyqx', '/g_BF', '/g_NBA2K',
            '/g_famine', '/g_DECEIT', '/g_lhcm', '/g_NMS', '/g_qmzz', '/g_AC', '/g_qmyks', '/g_RUST',
            '/g_hydbk', '/g_fs', '/g_zdfw', '/g_hddh', '/g_nnd', '/g_Scum', '/g_gjsd', '/g_wmkn',
            '/g_qjfs', '/g_sljt', '/g_jxjs', '/g_gmly', '/g_ryzh', '/g_SGZ', '/g_COD', '/g_twhj',
            '/g_dstjx', '/g_wztx', '/g_hyrzjjfbs', '/g_jpfc', '/g_ozkcmn', '/g_wm', '/g_ztsj', '/g_bfxxl',
            '/g_Foxhole',
        ]

        self.categorys_list_fanye = [
            '/2_270', '/2_19, ' '/ 2_26', ' / ', ' / ', ' / ', ' / ',' / ',
            '/', '/', '/', '/', '/', '/', '/', '/',
            '/', '/', '/', '/', '/', '/', '/', '/',
            '/', '/', '/', '/', '/', '/', '/', '/',
            '/', '/', '/', '/', '/', '/', '/', '/',
            '/',
        ]


    def get_url_list(self):
        for category in self.categorys_list:
            category_url = self.url_host + category
            self.url_list.append(category_url)

        return self.url_list

    def get_dict(self):
        url_dict = {}
        for category, fans in zip(self.categorys_list, self.categorys_list_fanye):
            url_dict[category] = fans
        return url_dict

    def get_host_info(self, url):
        dic = self.get_dict()
        p= 1
        data={}
        time.sleep(0.2)
        print('Now start open {}'.format(url))
        for i in range(3):
            try:
                wb_data = requests.get(url, headers=self.headers)
                break
            except:
                print('net work error! will retry 3 times')

        soup = BeautifulSoup(wb_data.text, 'lxml')

        # print(soup)
        print('start analazy url')
        try:
            category = soup.select('h1')[0].get_text()
        except:
            category = '未定義類別'
        names = soup.select('.ellipsis.fl')
        nums = soup.select('.dy-num.fr')                                 #anchor-info > div.relate-text.fl > div.acinfo-fs-con.clearfix > ul > li:nth-child(3) > a > div.hot-v-con > span
        titles = soup.select('.mes h3')
        hrefs = soup.select('#live-list-contentbox  li  a')
        for name, num, href, title in zip(names, nums, hrefs, titles):
            data = {
                '类別': category,
                '主播': name.get_text(),
                '标题': title.get_text().split('\n')[-1].strip(),
                '人氣指數': float(num.get_text()[:-1]) if '万' in num.get_text() else float(num.get_text()) / 10000,
                '房间id':href.get('href')[1:]
            }

            roomUrl = 'https://www.douyu.com/' + data['房间id']
            dy = driveSpider(roomUrl)
            #获取主播的hashname，可用于获取主页信息，视频信息
            authorurl = requests.get('https://www.douyu.com/swf_api/getRoomRecordStatus/%s'%(data['房间id'])).json()['data']['authorurl']
            data['hashname'] = authorurl[27:]
            if len(authorurl)>0:
                f = open('zhubo_home.txt', 'a')
                f.write(authorurl + '\n')
                f.close()
            data['周排名'], data['关注数目'], data['视频数目'], data['播放总量'], data['水友数目'],data['经验值'],data['巅峰值'] = dy.getItem()
            data.update(self.get_zhibo_info(data['房间id']))
            self.write_to_zhubo(data)
        if dic[url[22:]] !='/':
            self.get_zhubo_byApi()


    def get_zhubo_byApi(self):
        i = 2
        while True:
            apiUrl = 'https://www.douyu.com/gapi/rkc/directory/2_19/%i' % (i)
            print('当前第%i页' % (i))
            apiData = requests.get(apiUrl, headers=self.headers).json()['data']
            pageNum = apiData['pgcnt']
            print('一共%i页' % (pageNum))
            apiData = apiData['rl']
            category = apiData[0]['c2name']
            for data in apiData:
                tmp_data = {
                    '类別': category,
                    '主播': data['nn'],
                    '标题': data['rn'],
                    '人氣指數': data['ol'],
                    '房间id': data['rid']
                }
                roomUrl = 'https://www.douyu.com/' + str(data['房间id'])
                print(roomUrl)
                dy = driveSpider(roomUrl)
                tmp_data['周排名'], tmp_data['关注数目'], tmp_data['视频数目'], tmp_data['播放总量'], tmp_data['水友数目'] = dy.getItem()
                data = tmp_data
                data.update(self.get_zhibo_info(data['房间id']))

                authorurl = requests.get('https://www.douyu.com/swf_api/getRoomRecordStatus/%s' % (data['房间id'])).json()['data']['authorurl']
                data['hashname'] = authorurl[27:]
                if len(authorurl)>0:
                    f = open('zhubo_home.txt', 'a')
                    f.write(authorurl + '\n')
                    f.close()
                self.write_to_zhubo(data)
            if i < pageNum:
                i = i + 1
            else:
                break

    def write_to_zhubo(self,data):

        f = open("zhubo_info.csv", "a", newline="", encoding="utf-8")
        v = csv.writer(f)
        v.writerow(data.values())
        print(data)
        f.close()

    def get_zhibo_info(self,href):

        apiUrl = 'http://open.douyucdn.cn/api/RoomApi/room/' + href
        apiData = requests.get(apiUrl, headers=self.headers).json()['data']
        try:
            zhibo_data = {
                '最近开播时间': apiData['start_time'],
                '开播状态': apiData['room_status'],
                '直播间人数': apiData['online'],
                '直播间关注数目': apiData['fans_num'],
                '礼物详情': len(apiData['gift'])
            }
        except:
            zhibo_data={
                '最近开播时间': '',
                '开播状态': '',
                '直播间人数': '',
                '直播间关注数目': '',
                '礼物详情': ''

            }
            print('直播信息异常')
        return zhibo_data
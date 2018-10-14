import requests
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
import csv
import time
def get_fans_url():
    f = open('Author_Info/zhubo_info.csv', 'r', newline="", encoding="utf-8")
    v = csv.reader(f)
    house_list = [row[-1] for row in v]
    f.close()
    print(house_list)
    return house_list

def get_fans(url_list):
    driver = webdriver.Chrome(executable_path='Author_Info/chromedriver.exe')
    sleep_time = 3
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    }
    for url in url_list:
        host ='https://www.douyu.com/%s'%(url)
        driver.get(host)
        time.sleep(sleep_time)
        html = driver.page_source.encode('utf-8')
        selector = etree.HTML(html)
        fans_list = selector.xpath('//*[@id="mCSB_3_container"]/ul/li')
        for fan in fans_list:
            fan_text = fan.xpath('/text()')
            print(fan_text)
            f = open('fans_info.csv', 'a', newline="", encoding="utf-8")
            v = csv.writer(f)
            v.writerow(fan_text)

            f.close()





if __name__ == '__main__':
    url_list = get_fans_url()
    get_fans(url_list)
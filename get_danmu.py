import requests
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
import csv
import time
def get_shipin_url():
    f = open('shipin_info.csv', 'r', newline="", encoding="utf-8")
    v = csv.reader(f)
    shipin_list = [row[5] for row in v]
    f.close()
    print(shipin_list)
    return shipin_list

def get_fans(url_list):
    driver = webdriver.Chrome(executable_path='Author_Info/chromedriver.exe')
    sleep_time = 3
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    }
    host ='https://v.douyu.com/show/'
    for url in url_list:
        driver.get(host+url)
        time.sleep(sleep_time)
        html = driver.page_source.encode('utf-8')
        selector = etree.HTML(html)
        try:
            danmu_list = selector.xpath('//*[@id="barrageCont"]')['li']
        except:
            danmu_list=[]
            print('error')
        print(danmu_list)









def main():
    url_list = get_shipin_url()
    get_fans(url_list)

if __name__ == '__main__':
    main()


'''
by sunjifeng
主函数，入口

'''

from Author_Info.douyu import douyu_host_info
dy = douyu_host_info()





def main():
    url_list = dy.get_url_list()
    for url in url_list:
        dy.get_host_info(url)



if __name__ == '__main__':
    main()
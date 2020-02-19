#! -*- coding:utf-8 -*-
import datetime
import time

import pymysql
import requests
from lxml import etree
from selenium import webdriver


def get_first_page():

    url = 'https://realestate.yahoo.co.jp/used/mansion/search/06/27/271/'
    driver.get(url)
    time.sleep(3)

    html = driver.page_source
    return html





# 把首页和翻页处理？

def next_page():
    for i in range(1,70):  # selenium 循环翻页成功！
        driver.find_element_by_xpath('//*[@id="nextBuilding"]').click()
        time.sleep(5)
        html = driver.page_source
        return html



def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    big_list = []
    selector = etree.HTML(html)
    for item_n in range (1,30):
        element_xpath ='//*[@id="table_{0}"]/ul/li/div[2]/ul/li[2]/a/@href'.format(item_n)
        f_link = selector.xpath(element_xpath)
        for item in f_link:
            big_list.append(item)
    return big_list


        # 存储到MySQL中

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456',
                                 db='JapanHouse',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into osaka_oldflat (link) values (%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except StopIteration:
        pass





if __name__ == '__main__':

    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=options)

    html = get_first_page()
    content = parse_html(html)
    time.sleep(1)
    insertDB(content)
    while True:
        html = next_page()
        content = parse_html(html)
        insertDB(content)
        print(datetime.datetime.now())
        time.sleep(1)


# #
# create table osaka_oldflat(
# id int not null primary key auto_increment,
# link text
# ) engine=InnoDB  charset=utf8;
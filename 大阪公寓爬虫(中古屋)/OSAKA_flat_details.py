#! -*- coding:utf-8 -*-


import datetime
import re
import time

import pymysql
import requests
from lxml import etree
from requests.exceptions import RequestException

def call_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

# 正则和lxml混用
def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    big_list = []
    selector = etree.HTML(html)
    fullPrice = selector.xpath('//*[@id="loan"]/text()')
    f_fullPrice = remove_block(fullPrice)

    location = selector.xpath('//*[@id="wrapper"]/div[5]/main/div/div[1]/div[1]/div/div[1]/div[4]/div[2]/span/text()')
    communication = selector.xpath('//*[@id="wrapper"]/div[5]/main/div/div[1]/div[1]/div/div[1]/div[4]/div[4]/text()')
    layout = selector.xpath('//*[@id="wrapper"]/div[5]/main/div/div[1]/div[1]/div/div[1]/div[5]/ul/li[1]/div[2]/span/text()')
    square = selector.xpath('//*[@id="wrapper"]/div[5]/main/div/div[1]/div[1]/div/div[1]/div[5]/ul/li[2]/span/text()')
    f_squre = GetOneList(square)

    height = selector.xpath('//*[@id="wrapper"]/div[5]/main/div/div[1]/div[1]/div/div[1]/div[5]/ul/li[3]/span/text()')
    light_dire = selector.xpath('//*[@id="wrapper"]/div[5]/main/div/div[1]/div[1]/div/div[1]/div[5]/ul/li[4]/span/text()')
    houseHistory = selector.xpath('//*[@id="wrapper"]/div[5]/main/div/div[1]/div[1]/div/div[1]/div[5]/ul/li[5]/span/text()')




    try:

        long_tuple = (i for i in zip(f_fullPrice,location,communication,layout,f_squre[0],height,light_dire,houseHistory))
        for i in long_tuple:
            big_list.append(i)
        return big_list
    except IndexError as e:
        pass

def GetOneList(item):
    f_l = []
    for it in item:
        f_str = ["".join(it)]
        f_l.append(f_str)

    return f_l




def remove_block(items):
    new_items = []
    for it in items:
        f = "".join(it.split())
        new_items.append(f)
    return new_items




def Python_sel_Mysql():
    # 使用cursor()方法获取操作游标
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='JapanHouse',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cur = connection.cursor()
    #sql 语句
    for i in range(275,1762):
        sql = 'select link from osaka_oldflat where id = %s ' % i
        # #执行sql语句
        cur.execute(sql)
        # #获取所有记录列表
        data = cur.fetchone()
        url = data['link']
        yield url

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='JapanHouse',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    try:
        cursor.executemany('insert into osaka_oldflat_detail (f_fullPrice,location,communication,layout,f_squre,height,light_dire,houseHistory) values (%s,%s,%s,%s,%s,%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError :
        pass



if __name__ == '__main__':
    for url_str in Python_sel_Mysql():
        html = call_page(url_str)
        try:

            content = parse_html(html)
            insertDB(content)
            print(content)
            print(datetime.datetime.now())

        except ValueError :
            pass




# f_fullPrice,location,communication,layout,f_squre,height,light_dire,houseHistory
# create table osaka_oldflat_detail(
# id int not null primary key auto_increment,
# f_fullPrice varchar(80),
# location varchar(80),
# communication varchar(88),
# layout varchar(88),
# f_squre varchar(88),
# height varchar(88),
# light_dire varchar(88),
# houseHistory varchar(88)
# ) engine=InnoDB  charset=utf8;


# drop table osaka_oldflat_detail;

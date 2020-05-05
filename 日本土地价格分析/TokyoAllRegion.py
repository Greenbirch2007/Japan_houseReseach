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

def RemoveDot(item):
    f_l = []
    for it in item:

        f_str = "".join(it.split(","))
        ff_str = f_str
        f_l.append(ff_str)

    return f_l

def remove_douhao(num):
    num1 = "".join(num.split(","))
    f_num = str(num1)
    return f_num

# 正则和lxml混用
def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    big_list = []
    selector = etree.HTML(html)
    Region_Name = selector.xpath('//*[@id="Top"]/h1/text()')
    Region_Ave = selector.xpath('//*[@id="Top_Chika_Common"]/text()')
    Region_OnePrice = selector.xpath('//*[@id="List_UL"]/li/ul/li[1]/b/text()')
    _Region_Ave = RemoveDot(Region_Ave)
    _Region_OnePrice = RemoveDot(Region_OnePrice)
    f_OneName = []
    for num in range(1,len(Region_OnePrice)*2,2):
        Region_OneName = selector.xpath('//*[@id="List_UL"]/li[{0}]/text()'.format(num))
        f_OneName.append(Region_OneName)
    f_Region_Name = len(Region_OnePrice)*Region_Name
    f_Region_Ave = len(Region_OnePrice)*_Region_Ave

    try:

        long_tuple = (i for i in zip(f_Region_Name,f_Region_Ave,f_OneName,_Region_OnePrice))
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











def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='JapanHouse',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    try:
        cursor.executemany('insert into tokyo_GroundPrice (r_name,r_nameAveP,r_OneName,r_OnePrice) values (%s,%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError :
        pass



if __name__ == '__main__':
    all_r =["http://cn.tochidai.info/tokyo/chiyoda/","http://cn.tochidai.info/tokyo/chuo/","http://cn.tochidai.info/tokyo/minato/","http://cn.tochidai.info/tokyo/shinjuku/","http://cn.tochidai.info/tokyo/bunkyo/","http://cn.tochidai.info/tokyo/taito/","http://cn.tochidai.info/tokyo/sumida/","http://cn.tochidai.info/tokyo/koto/","http://cn.tochidai.info/tokyo/shinagawa/","http://cn.tochidai.info/tokyo/meguro/","http://cn.tochidai.info/tokyo/ota/","http://cn.tochidai.info/tokyo/setagaya/","http://cn.tochidai.info/tokyo/shibuya/","http://cn.tochidai.info/tokyo/nakano/","http://cn.tochidai.info/tokyo/suginami/","http://cn.tochidai.info/tokyo/toshima/","http://cn.tochidai.info/tokyo/kita/","http://cn.tochidai.info/tokyo/arakawa/","http://cn.tochidai.info/tokyo/itabashi/","http://cn.tochidai.info/tokyo/nerima/","http://cn.tochidai.info/tokyo/adachi/","http://cn.tochidai.info/tokyo/katsushika/","http://cn.tochidai.info/tokyo/edogawa/","http://cn.tochidai.info/tokyo/hachioji/","http://cn.tochidai.info/tokyo/tachikawa/","http://cn.tochidai.info/tokyo/musashino/","http://cn.tochidai.info/tokyo/mitaka/","http://cn.tochidai.info/tokyo/ome/","http://cn.tochidai.info/tokyo/fuchu/","http://cn.tochidai.info/tokyo/akishima/","http://cn.tochidai.info/tokyo/chofu/","http://cn.tochidai.info/tokyo/machida/","http://cn.tochidai.info/tokyo/koganei/","http://cn.tochidai.info/tokyo/kodaira/","http://cn.tochidai.info/tokyo/hino/","http://cn.tochidai.info/tokyo/higashimurayama/","http://cn.tochidai.info/tokyo/kokubunji/","http://cn.tochidai.info/tokyo/kunitachi/","http://cn.tochidai.info/tokyo/fussa/","http://cn.tochidai.info/tokyo/komae/","http://cn.tochidai.info/tokyo/higashiyamato/","http://cn.tochidai.info/tokyo/kiyose/","http://cn.tochidai.info/tokyo/higashikurume/","http://cn.tochidai.info/tokyo/musashimurayama/","http://cn.tochidai.info/tokyo/tama/","http://cn.tochidai.info/tokyo/inagi/","http://cn.tochidai.info/tokyo/hamura/","http://cn.tochidai.info/tokyo/akiruno/","http://cn.tochidai.info/tokyo/nishitokyo/","http://cn.tochidai.info/tokyo/mizuho/","http://cn.tochidai.info/tokyo/hinode/","http://cn.tochidai.info/tokyo/hinohara/","http://cn.tochidai.info/tokyo/okutama/","http://cn.tochidai.info/tokyo/oshima/","http://cn.tochidai.info/tokyo/toshimamura/","http://cn.tochidai.info/tokyo/niijima/","http://cn.tochidai.info/tokyo/kozushima/","http://cn.tochidai.info/tokyo/miyake/","http://cn.tochidai.info/tokyo/mikurajima/","http://cn.tochidai.info/tokyo/hachijo/","http://cn.tochidai.info/tokyo/aogashima/","http://cn.tochidai.info/tokyo/ogasawara/" ]



    for url_str in all_r:
        html = call_page(url_str)
        try:

            content = parse_html(html)
            # insertDB(content)
            print(content)
            print(datetime.datetime.now())

        except ValueError :
            pass




# r_name,r_nameAveP,r_OneName,r_OnePrice
# create table tokyo_GroundPrice(
# id int not null primary key auto_increment,
# r_name varchar(80),
# r_nameAveP bigint(20),
# r_OneName varchar(88),
# r_OnePrice bigint(20)
# ) engine=InnoDB  charset=utf8;


# drop table tokyo_GroundPrice;

#  select * from tokyo_GroundPrice order by r_OnePrice desc limit 20;
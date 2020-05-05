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
        cursor.executemany('insert into Osaka_GroundPrice (r_name,r_nameAveP,r_OneName,r_OnePrice) values (%s,%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError :
        pass



if __name__ == '__main__':
    all_r =["http://cn.tochidai.info/osaka/","http://cn.tochidai.info/osaka/osaka-miyakojima/","http://cn.tochidai.info/osaka/osaka-fukushima/","http://cn.tochidai.info/osaka/osaka-konohana/","http://cn.tochidai.info/osaka/osaka-nishi/","http://cn.tochidai.info/osaka/osaka-minato/","http://cn.tochidai.info/osaka/osaka-taisho/","http://cn.tochidai.info/osaka/osaka-tennoji/","http://cn.tochidai.info/osaka/osaka-naniwa/","http://cn.tochidai.info/osaka/osaka-nishiyodogawa/","http://cn.tochidai.info/osaka/osaka-higashiyodogawa/","http://cn.tochidai.info/osaka/osaka-higashinari/","http://cn.tochidai.info/osaka/osaka-ikuno/","http://cn.tochidai.info/osaka/osaka-asahi/","http://cn.tochidai.info/osaka/osaka-joto/","http://cn.tochidai.info/osaka/osaka-abeno/","http://cn.tochidai.info/osaka/osaka-sumiyoshi/","http://cn.tochidai.info/osaka/osaka-higashisumiyoshi/","http://cn.tochidai.info/osaka/osaka-nishinari/","http://cn.tochidai.info/osaka/osaka-yodogawa/","http://cn.tochidai.info/osaka/osaka-tsurumi/","http://cn.tochidai.info/osaka/osaka-suminoe/","http://cn.tochidai.info/osaka/osaka-hirano/","http://cn.tochidai.info/osaka/osaka-kita/","http://cn.tochidai.info/osaka/osaka-chuo/","http://cn.tochidai.info/osaka/sakai/","http://cn.tochidai.info/osaka/sakai-sakai/","http://cn.tochidai.info/osaka/sakai-naka/","http://cn.tochidai.info/osaka/sakai-higashi/","http://cn.tochidai.info/osaka/sakai-nishi/","http://cn.tochidai.info/osaka/sakai-minami/","http://cn.tochidai.info/osaka/sakai-kita/","http://cn.tochidai.info/osaka/sakai-mihara/","http://cn.tochidai.info/osaka/kishiwada/","http://cn.tochidai.info/osaka/toyonaka/","http://cn.tochidai.info/osaka/ikeda/","http://cn.tochidai.info/osaka/suita/","http://cn.tochidai.info/osaka/izumiotsu/","http://cn.tochidai.info/osaka/takatsuki/","http://cn.tochidai.info/osaka/kaizuka/","http://cn.tochidai.info/osaka/moriguchi/","http://cn.tochidai.info/osaka/hirakata/","http://cn.tochidai.info/osaka/ibaraki/","http://cn.tochidai.info/osaka/yao/","http://cn.tochidai.info/osaka/izumisano/","http://cn.tochidai.info/osaka/tondabayashi/","http://cn.tochidai.info/osaka/neyagawa/","http://cn.tochidai.info/osaka/kawachinagano/","http://cn.tochidai.info/osaka/matsubara/","http://cn.tochidai.info/osaka/daito/","http://cn.tochidai.info/osaka/izumi/","http://cn.tochidai.info/osaka/minoh/","http://cn.tochidai.info/osaka/kashiwara/","http://cn.tochidai.info/osaka/habikino/","http://cn.tochidai.info/osaka/kadoma/","http://cn.tochidai.info/osaka/settsu/","http://cn.tochidai.info/osaka/takaishi/","http://cn.tochidai.info/osaka/fujiidera/","http://cn.tochidai.info/osaka/higashiosaka/","http://cn.tochidai.info/osaka/sennan/","http://cn.tochidai.info/osaka/shijonawate/","http://cn.tochidai.info/osaka/katano/","http://cn.tochidai.info/osaka/osakasayama/","http://cn.tochidai.info/osaka/hannan/","http://cn.tochidai.info/osaka/shimamoto/","http://cn.tochidai.info/osaka/toyono/","http://cn.tochidai.info/osaka/nose/","http://cn.tochidai.info/osaka/tadaoka/","http://cn.tochidai.info/osaka/kumatori/","http://cn.tochidai.info/osaka/tajiri/","http://cn.tochidai.info/osaka/misaki/","http://cn.tochidai.info/osaka/taishi/","http://cn.tochidai.info/osaka/kanan/","http://cn.tochidai.info/osaka/chihayaakasaka/"]




    for url_str in all_r:
        html = call_page(url_str)
        try:

            content = parse_html(html)
            insertDB(content)
            print(content)
            print(datetime.datetime.now())

        except ValueError :
            pass




# r_name,r_nameAveP,r_OneName,r_OnePrice
# create table Osaka_GroundPrice(
# id int not null primary key auto_increment,
# r_name varchar(80),
# r_nameAveP bigint(20),
# r_OneName varchar(88),
# r_OnePrice bigint(20)
# ) engine=InnoDB  charset=utf8;


# drop table Osaka_GroundPrice;

#  select * from Osaka_GroundPrice order by r_OnePrice desc limit 20;
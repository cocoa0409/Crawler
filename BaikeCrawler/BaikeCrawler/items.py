# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import pymysql
import logging
from scrapy import Item,Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join

class BaikePageItem(Item):
    topic = Field(
        input_processor=Join(''),
        output_processor=Join('')
    )
    topic_url = Field(
        input_processor=Join(''),
        output_processor=Join('')
    )
    #为了提取整段text
    detail_text = Field(
        input_processor = Join(''),
        output_processor = Join('')
    )

    def insert_data(self,item):
        ##返回说明：返回2代表更新数据，同url，不同的topic
        ##返回说明：返回1代表新插入数据,数据库中原来无此同topic 不同url，此时对应pipline应返回True，输出json
        ##         返回0代表更新数据，数据库中原来有此数据，此时对应pipline应返回False，不输出json
        if 'topic' in item.keys() and 'detail_text' in item.keys():
            try:
                sql="insert into pageinfo(page_topic,page_url) VALUES (\'"+item['topic']+"\',\'"+item['topic_url']+"\') on DUPLICATE KEY UPDATE page_url=values(page_url),page_topic=values(page_topic);"
                flag = MySQLConnect.mysql_sure_duplicated(sql)
            except:
                sql='insert into pageinfo(page_topic,page_url) VALUES (\"'+item['topic']+'\",\"'+item['topic_url']+'\") on DUPLICATE KEY UPDATE page_url=values(page_url),page_topic=values(page_topic);'
                flag = MySQLConnect.mysql_sure_duplicated(sql)
            if flag == 1  or flag == 2 :
                return True
            elif flag == 0:
                return False
            else:
                logging.log(logging.ERROR,"ERROR found in insert_data(state): "+flag+' '+item['topic_url']+' '+item['topic'])
                return False
        else:
            # if 'topic' not in item.keys():
            #     logging.log(logging.ERROR, "  topic Unknown (throw away): " + item['topic_url'])
            # elif 'detail_text' not in item.keys():
            #     logging.log(logging.ERROR, "  detail_text Unknown (throw away): " + item['topic_url'])
            return False


class BaikePageLoader(ItemLoader):
    default_output_processor = Join('')
    default_input_processor = Join('')


class MySQLConnect(Item):
    @staticmethod
    def mysqlConnect(sql):
        host= '127.0.0.1'
        user = 'root'
        # 你自己数据库的密码
        psd= 'Mama1203.'
        port = 3306
        # 你自己数据库的名称
        db = 'scrapydb'
        charset = 'utf8'
        # 数据库连接
        con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=charset, port=port)
    # 数据库游标
        cur = con.cursor()
        result=cur.execute(sql)
        con.commit()
        con.close()
        return result


    @staticmethod
# 1. insert      on duplicate key update
    ##返回说明：返回2代表更新数据,数据库中原来无此数据
    ##         返回1代表新插入数据，数据库中原来含有同topic，但不同的url的数据
    ##         返回0代表更新数据，数据库中原来有此数据
# 2. select * from pageinfo where page_topic=" ";
    ##返回说明：返回0代表无此数据
    ##         返回1代表有此数据
    def mysql_sure_duplicated(sql):
        host = '127.0.0.1'
        user = 'root'
        # 你自己数据库的密码
        psd = 'Mama1203.'
        port = 3306
        # 你自己数据库的名称
        db = 'scrapydb'
        charset = 'utf8'
        # 数据库连接
        con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=charset, port=port)
        # 数据库游标
        cur = con.cursor()
        result = cur.execute(sql)
        con.commit()
        con.close()
        return result


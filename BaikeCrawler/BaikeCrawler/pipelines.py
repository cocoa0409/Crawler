# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from .items import BaikePageItem
from scrapy import signals
from scrapy.exporters import JsonItemExporter,JsonLinesItemExporter,XmlItemExporter
import random,string
import redis

class BaikecrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

#调用api写入json的pipline
class JSONLineExportPipeline(object):
    def __init__(self):
        # self.is_seen=set()
        self.file_page = open('/Users/choukichiou/Desktop/BaikeCrawler/output_files/JSON_'+''.join(random.sample(string.ascii_letters + string.digits, 8))+'.json', 'wb')
    @classmethod
    def from_crawler(cls, crawler):
         pipeline = cls()
         crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
         crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
         return pipeline

    def spider_opened(self, spider):
        self.exporter_page = JsonLinesItemExporter(self.file_page,ensure_ascii=False)
        self.exporter_page.start_exporting()

    def spider_closed(self, spider):
        self.exporter_page.finish_exporting()
        self.file_page.close()

    def process_item(self, item, spider):
        # if(isinstance(item,BaikePageItem)):
        #     if(item['topic'] not in self.is_seen):
        #         self.is_seen.add(item['topic'])
        #         self.exporter_page.export_item(item)
        #     else:
        #         raise DropItem("redundent page found")
        self.exporter_page.export_item(item)
        return item




class MySqlRecordPipeline(object):
    def process_item(self,item,spider):
        Flag = item.insert_data(item)
        if Flag == False:
            raise DropItem("duplicated page in MySql found")
        return item



class RedisRecordPipeline(object):
    def __init__(self):
        self.r = redis.Redis(host="r-2zefaf7b49aed5e4.redis.rds.aliyuncs.com",port=6379,db=18,password="uXAqvbX5LR")

    def process_item(self,item,spider):
        result = self.r.sadd("baike","https://baike.baidu.com"+item['topic_url'])
        if result == 1:
            return item
        else:
            raise DropItem("drop item")
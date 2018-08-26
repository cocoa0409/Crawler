import sys
import urllib
import re

from scrapy import Request
from scrapy.http import HtmlResponse
from scrapy.loader.processors import TakeFirst, MapCompose
from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.linkextractors import LinkExtractor

from ..utils import changeLinkformat, get_start_urls_from_unknown_links
from ..items import BaikePageItem,BaikePageLoader,MySQLConnect
from scrapy import log
import logging


# #百科分类
# "https://baike.baidu.com/item/%E8%87%AA%E7%84%B6/1531",
# "https://baike.baidu.com/item/%E6%96%87%E5%8C%96/23624",
# "https://baike.baidu.com/item/%E5%9C%B0%E7%90%86/176780",
# "https://baike.baidu.com/item/%E5%8E%86%E5%8F%B2/360",
# "https://baike.baidu.com/item/%E7%94%9F%E6%B4%BB/18684",
# "https://baike.baidu.com/item/%E7%A4%BE%E4%BC%9A/73320",
# "https://baike.baidu.com/item/%E8%89%BA%E6%9C%AF/12004323",
# "https://baike.baidu.com/item/%E4%BA%BA%E7%89%A9/5957728",
# "https://baike.baidu.com/item/%E7%BB%8F%E6%B5%8E",
# "https://baike.baidu.com/item/%E7%A7%91%E5%AD%A6%E6%8A%80%E6%9C%AF",
# "https://baike.baidu.com/item/%E4%BD%93%E8%82%B2",
# "https://baike.baidu.com/item/%E7%BB%8F%E6%B5%8E%E5%AD%A6%E5%8D%81%E5%A4%A7%E5%8E%9F%E7%90%86/8771596",
# #得到分类
# "https://baike.baidu.com/item/%E6%96%87%E5%AD%A6/6437",
# "https://baike.baidu.com/item/%E5%93%B2%E5%AD%A6/140608",
# "https://baike.baidu.com/item/%E7%A4%BE%E4%BC%9A%E5%AD%A6/283098?fr=aladdin",
# "https://baike.baidu.com/item/%E6%94%BF%E6%B2%BB",
# "https://baike.baidu.com/item/%E6%95%99%E8%82%B2",
# "https://baike.baidu.com/item/%E9%87%91%E8%9E%8D/860",
# "https://baike.baidu.com/item/%E7%AE%A1%E7%90%86/366755",
# "https://baike.baidu.com/item/%E6%95%B0%E5%AD%A6/107037",
# "https://baike.baidu.com/item/%E7%89%A9%E7%90%86%E5%AD%A6/313183",
# "https://baike.baidu.com/item/%E7%94%9F%E7%89%A9%E5%AD%A6/1358",
# "https://baike.baidu.com/item/%E5%8C%BB%E5%AD%A6",
# "https://baike.baidu.com/item/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%A7%91%E5%AD%A6/9132",
# "https://baike.baidu.com/item/%E5%A4%A9%E6%96%87%E5%AD%A6",
# "https://baike.baidu.com/item/%E8%81%8C%E5%9C%BA",
# "https://baike.baidu.com/item/%E7%A4%BE%E4%BA%A4",
# "https://baike.baidu.com/item/%E5%AE%B6%E5%BA%AD/2221140",
# "https://baike.baidu.com/item/%E4%B8%96%E7%95%8C%E5%90%84%E5%9B%BD",

class BaikeSpider(CrawlSpider):
    name = "bkpage"
    # start_urls = get_start_urls_from_unknown_links()
    start_urls = [
         # 经济学
        "https://baike.baidu.com/item/%E5%AE%8F%E8%A7%82%E7%BB%8F%E6%B5%8E%E5%AD%A6/27041",
        "https://baike.baidu.com/item/%E8%AE%A1%E9%87%8F%E7%BB%8F%E6%B5%8E%E5%AD%A6/80374",
        "https://baike.baidu.com/item/%E5%8D%9A%E5%BC%88%E8%AE%BA/81545",
        "https://baike.baidu.com/item/%E8%A5%BF%E6%96%B9%E7%BB%8F%E6%B5%8E%E5%AD%A6/932",
        #经济学标签集合
        "https://baike.baidu.com/item/%E7%AD%9B%E9%80%89",
        "https://baike.baidu.com/item/%E4%BA%A4%E6%98%93%E6%88%90%E6%9C%AC",
        "https://baike.baidu.com/item/%E5%B8%82%E5%9C%BA%E5%8A%9B%E9%87%8F",
        "https://baike.baidu.com/item/%E5%B0%B1%E4%B8%9A",
        "https://baike.baidu.com/item/%E5%85%AC%E5%85%B1%E9%80%89%E6%8B%A9",
        "https://baike.baidu.com/item/%E4%B8%AA%E4%BA%BA%E6%94%B6%E5%85%A5",
        "https://baike.baidu.com/item/%E5%BC%B9%E6%80%A7/6371513",
        "https://baike.baidu.com/item/%E9%87%91%E8%9E%8D%E5%B8%82%E5%9C%BA/329967",
        "https://baike.baidu.com/item/%E5%85%AC%E5%8F%B8",
        "https://baike.baidu.com/item/%E7%BB%8F%E6%B5%8E%E5%A2%9E%E9%95%BF/81517",
        "https://baike.baidu.com/item/%E8%90%A7%E6%9D%A1",
        "https://baike.baidu.com/item/%E5%88%86%E9%85%8D/5577768",
        "https://baike.baidu.com/item/%E5%8E%82%E5%95%86",
        "https://baike.baidu.com/item/%E8%B5%AB%E8%8A%AC%E8%BE%BE%E5%B0%94%E2%80%94%E8%B5%AB%E5%B8%8C%E6%9B%BC%E6%8C%87%E6%95%B0/1429385",
        "https://baike.baidu.com/item/%E7%A6%8F%E5%88%A9%E7%BB%8F%E6%B5%8E%E5%AD%A6/85535",
        "https://baike.baidu.com/item/%E5%9B%BA%E5%AE%9A%E6%88%90%E6%9C%AC",
        "https://baike.baidu.com/item/%E4%B9%98%E6%95%B0/2575947",
        "https://baike.baidu.com/item/%E8%B5%84%E6%9C%AC%E4%B8%BB%E4%B9%89/87961",
        "https://baike.baidu.com/item/%E6%8A%98%E7%8E%B0",
        "https://baike.baidu.com/item/%E7%94%9F%E4%BA%A7%E5%87%BD%E6%95%B0",
        "https://baike.baidu.com/item/%E5%87%AF%E6%81%A9%E6%96%AF%E5%AD%A6%E6%B4%BE",
        "https://baike.baidu.com/item/%E8%BE%B9%E9%99%85%E6%95%88%E7%94%A8",
        "https://baike.baidu.com/item/%E8%87%AA%E7%84%B6%E5%A4%B1%E4%B8%9A%E7%8E%87",
        "https://baike.baidu.com/item/%E6%9C%BA%E4%BC%9A%E6%88%90%E6%9C%AC",
        "https://baike.baidu.com/item/%E6%B4%BB%E6%9C%9F%E5%AD%98%E6%AC%BE",
        "https://baike.baidu.com/item/%E8%B4%A7%E5%B8%81%E6%95%B0%E9%87%8F%E8%AE%BA",
        "https://baike.baidu.com/item/%E6%8A%95%E8%B5%84%E9%9C%80%E6%B1%82",
        "https://baike.baidu.com/item/%E6%B5%81%E5%8A%A8%E6%80%A7",
        "https://baike.baidu.com/item/%E4%BF%9D%E9%99%A9/262",
        "https://baike.baidu.com/item/%E6%81%B6%E6%80%A7%E9%80%9A%E8%B4%A7%E8%86%A8%E8%83%80",
        "https://baike.baidu.com/item/%E5%9D%87%E8%A1%A1%E4%BB%B7%E6%A0%BC",
        "https://baike.baidu.com/item/%E6%9C%89%E6%95%88%E5%B8%82%E5%9C%BA%E5%81%87%E8%AF%B4",
        "https://baike.baidu.com/item/%E8%B4%B4%E7%8E%B0%E7%8E%87",
        "https://baike.baidu.com/item/%E9%A3%8E%E9%99%A9%E5%88%86%E6%91%8A",
        "https://baike.baidu.com/item/%E4%BB%B7%E6%A0%BC",
        "https://baike.baidu.com/item/%E6%B1%87%E7%8E%87",
        "https://baike.baidu.com/item/%E4%BA%A7%E5%87%BA",
        "https://baike.baidu.com/item/%E6%97%A0%E9%99%90%E8%B4%A3%E4%BB%BB",
        "https://baike.baidu.com/item/%E6%AF%94%E8%BE%83%E4%BC%98%E5%8A%BF",
        "https://baike.baidu.com/item/%E5%90%8D%E4%B9%89%E5%88%A9%E7%8E%87",
        "https://baike.baidu.com/item/%E6%B3%95%E5%AE%9A%E5%87%86%E5%A4%87%E9%87%91%E7%8E%87",
        "https://baike.baidu.com/item/%E5%9B%BA%E5%AE%9A%E8%B5%84%E4%BA%A7%E6%8A%98%E6%97%A7?fromtitle=%E6%8A%98%E6%97%A7&fromid=2461531",
        "https://baike.baidu.com/item/%E7%A4%BE%E4%BC%9A%E4%B8%BB%E4%B9%89/296",
        "https://baike.baidu.com/item/%E7%90%86%E6%80%A7%E4%BA%BA",
        "https://baike.baidu.com/item/%E5%BE%AE%E8%A7%82%E7%BB%8F%E6%B5%8E%E5%AD%A6/1702",
        "https://baike.baidu.com/item/%E5%A4%96%E6%BA%A2",
        "https://baike.baidu.com/item/%E9%80%9A%E8%B4%A7%E7%B4%A7%E7%BC%A9/529",
        "https://baike.baidu.com/item/%E5%87%80%E6%8D%9F%E5%A4%B1",
        "https://baike.baidu.com/item/%E5%8F%91%E6%98%8E/1615352",
        "https://baike.baidu.com/item/%E6%B7%B7%E5%90%88%E7%BB%8F%E6%B5%8E",
        "https://baike.baidu.com/item/%E4%BA%BA%E5%8A%9B%E8%B5%84%E6%9C%AC/248509",
        "https://baike.baidu.com/item/%E6%94%B6%E7%9B%8A",
        "https://baike.baidu.com/item/%E4%BA%A7%E4%B8%9A",
        "https://baike.baidu.com/item/%E5%AE%9E%E8%AF%81%E7%BB%8F%E6%B5%8E%E5%AD%A6",
        "https://baike.baidu.com/item/%E6%8E%92%E4%BB%96%E6%80%A7",
        "https://baike.baidu.com/item/%E8%BE%B9%E9%99%85%E6%88%90%E6%9C%AC",
        "https://baike.baidu.com/item/%E5%B9%B2%E9%A2%84",
        "https://baike.baidu.com/item/%E9%80%9A%E8%B4%A7",
        "https://baike.baidu.com/item/%E5%8F%91%E5%B1%95%E4%B8%AD%E5%9B%BD%E5%AE%B6",
        "https://baike.baidu.com/item/%E9%A3%8E%E9%99%A9%E8%A7%84%E9%81%BF",
        "https://baike.baidu.com/item/%E5%85%BC%E5%B9%B6/5615094",
        "https://baike.baidu.com/item/%E7%94%9F%E4%BA%A7%E8%80%85%E5%89%A9%E4%BD%99",
        "https://baike.baidu.com/item/%E6%8C%A4%E5%87%BA%E6%95%88%E5%BA%94",
        "https://baike.baidu.com/item/%E5%88%A9%E7%8E%87",
        "https://baike.baidu.com/item/%E8%8F%B2%E5%88%A9%E6%99%AE%E6%96%AF%E6%9B%B2%E7%BA%BF",
        "https://baike.baidu.com/item/%E7%A6%8F%E5%88%A9/2877",
        "https://baike.baidu.com/item/%E8%87%AA%E7%94%B1%E8%B4%B8%E6%98%93",
        "https://baike.baidu.com/item/%E8%B5%84%E6%9C%AC/1015076",
        "https://baike.baidu.com/item/%E6%9C%80%E7%BB%88%E4%BA%A7%E5%93%81",
        "https://baike.baidu.com/item/%E5%B9%B3%E5%9D%87%E4%BA%A7%E9%87%8F",
        "https://baike.baidu.com/item/%E8%BE%B9%E9%99%85%E7%A8%8E%E7%8E%87",
        "https://baike.baidu.com/item/%E4%B8%93%E5%88%A9",
        "https://baike.baidu.com/item/%E6%97%A0%E5%B7%AE%E5%BC%82%E6%9B%B2%E7%BA%BF",
        "https://baike.baidu.com/item/%E8%B4%AC%E5%80%BC",
        "https://baike.baidu.com/item/%E7%8E%B0%E5%80%BC",
        "https://baike.baidu.com/item/%E5%8F%91%E4%BF%A1%E5%8F%B7",
        "https://baike.baidu.com/item/%E9%80%9A%E8%B4%A7%E8%86%A8%E8%83%80",
        "https://baike.baidu.com/item/%E8%B5%84%E4%BA%A7%E8%B4%9F%E5%80%BA%E8%A1%A8",
        "https://baike.baidu.com/item/%E9%9C%80%E6%B1%82%E6%9B%B2%E7%BA%BF",
        "https://baike.baidu.com/item/%E7%BB%8F%E6%B5%8E%E7%A7%9F",
        "https://baike.baidu.com/item/%E9%9C%80%E6%B1%82%E9%87%8F",
        "https://baike.baidu.com/item/%E8%BE%B9%E9%99%85%E6%94%B6%E7%9B%8A",
        "https://baike.baidu.com/item/%E7%9C%9F%E5%AE%9E%E5%88%A9%E7%8E%87",
        "https://baike.baidu.com/item/%E7%BB%8F%E6%B5%8E%E6%95%88%E7%8E%87",
        "https://baike.baidu.com/item/%E8%87%AA%E7%94%B1%E6%94%BE%E4%BB%BB",
        "https://baike.baidu.com/item/%E5%88%A9%E6%B6%A6",
        "https://baike.baidu.com/item/%E5%8D%A1%E7%89%B9%E5%B0%94/505189",
        "https://baike.baidu.com/item/%E4%B8%AD%E5%A4%AE%E9%93%B6%E8%A1%8C",
        "https://baike.baidu.com/item/%E4%BB%A3%E7%90%86%E4%BA%BA/67417",
        "https://baike.baidu.com/item/%E5%9E%84%E6%96%AD/649481",
        "https://baike.baidu.com/item/%E8%B4%A2%E6%94%BF%E6%94%BF%E7%AD%96",
        "https://baike.baidu.com/item/%E8%B4%A7%E5%B8%81%E6%94%BF%E7%AD%96/2575115",
        "https://baike.baidu.com/item/%E5%BD%92%E5%AE%BF/69556",
        "https://baike.baidu.com/item/%E7%A4%BE%E4%BC%9A%E4%BF%9D%E9%9A%9C/489",
        "https://baike.baidu.com/item/%E6%B2%89%E6%B2%A1%E6%88%90%E6%9C%AC",
        "https://baike.baidu.com/item/%E8%B4%B8%E6%98%93%E6%94%BF%E7%AD%96",
        "https://baike.baidu.com/item/%E9%A3%8E%E9%99%A9%E5%8E%8C%E6%81%B6",
        "https://baike.baidu.com/item/%E5%A4%96%E9%83%A8%E6%80%A7",
        "https://baike.baidu.com/item/%E5%B8%82%E5%9C%BA%E4%BB%BD%E9%A2%9D",
        "https://baike.baidu.com/item/%E5%9B%BD%E6%B0%91%E7%94%9F%E4%BA%A7%E6%80%BB%E5%80%BC",
        "https://baike.baidu.com/item/%E6%95%88%E7%8E%87%E5%B7%A5%E8%B5%84",
        "https://baike.baidu.com/item/%E7%AE%A1%E5%88%B6/40681",
        "https://baike.baidu.com/item/%E6%80%BB%E6%94%B6%E7%9B%8A",
        "https://baike.baidu.com/item/%E6%B6%88%E8%B4%B9/5800867",
        "https://baike.baidu.com/item/%E5%AE%9E%E9%99%85%E5%88%A9%E7%8E%87",
        "https://baike.baidu.com/item/%E7%A7%91%E6%96%AF%E5%AE%9A%E7%90%86",
        "https://baike.baidu.com/item/%E5%A4%B1%E4%B8%9A%E7%8E%87",
        "https://baike.baidu.com/item/%E5%B9%B3%E5%9D%87%E6%94%B6%E7%9B%8A",
        "https://baike.baidu.com/item/%E7%BD%A2%E5%B7%A5/19770",
        "https://baike.baidu.com/item/%E5%87%86%E5%A4%87%E9%87%91",
        "https://baike.baidu.com/item/%E5%B8%82%E5%9C%BA%E5%A4%B1%E7%81%B5",
        "https://baike.baidu.com/item/%E7%A6%8F%E5%88%A9%E5%9B%BD%E5%AE%B6",
        "https://baike.baidu.com/item/%E8%82%A1%E7%A5%A8%E5%B8%82%E5%9C%BA",
        "https://baike.baidu.com/item/%E8%8A%9D%E5%8A%A0%E5%93%A5%E5%AD%A6%E6%B4%BE",
        "https://baike.baidu.com/item/%E6%94%BF%E5%BA%9C%E5%80%BA%E5%8A%A1",
        "https://baike.baidu.com/item/%E4%BF%A1%E6%81%AF%E4%B8%8D%E5%AF%B9%E7%A7%B0",
        "https://baike.baidu.com/item/%E7%9F%AD%E6%9C%9F",
        "https://baike.baidu.com/item/%E7%94%9F%E4%BA%A7%E7%8E%87",
        "https://baike.baidu.com/item/%E8%8F%9C%E5%8D%95%E6%88%90%E6%9C%AC",
        "https://baike.baidu.com/item/%E9%85%8D%E9%A2%9D",
        "https://baike.baidu.com/item/%E7%9F%AD%E7%BC%BA",
        "https://baike.baidu.com/item/%E7%B4%AF%E8%BF%9B%E7%A8%8E",
        "https://baike.baidu.com/item/%E8%BE%B9%E9%99%85%E6%94%B6%E7%9B%8A%E9%80%92%E5%87%8F%E8%A7%84%E5%BE%8B",
        "https://baike.baidu.com/item/%E5%85%AC%E5%85%B1%E5%93%81",
        "https://baike.baidu.com/item/%E8%B4%9F%E5%80%BA/781271",
        "https://baike.baidu.com/item/%E6%95%88%E7%94%A8",
        "https://baike.baidu.com/item/%E5%9E%84%E6%96%AD%E4%BC%81%E4%B8%9A",
        "https://baike.baidu.com/item/%E6%B3%95%E5%AE%9A%E5%87%86%E5%A4%87%E9%87%91",
        "https://baike.baidu.com/item/%E5%9B%BA%E5%AE%9A%E6%B1%87%E7%8E%87",
        "https://baike.baidu.com/item/%E6%9B%BF%E4%BB%A3%E5%93%81/8249884",
        "https://baike.baidu.com/item/%E5%85%B3%E7%A8%8E",
        "https://baike.baidu.com/item/%E8%82%A1%E7%A5%A8/22647",
        "https://baike.baidu.com/item/%E8%87%AA%E7%84%B6%E5%9E%84%E6%96%AD",
        "https://baike.baidu.com/item/%E8%87%AA%E7%94%B1%E4%B8%BB%E4%B9%89/1587",
        "https://baike.baidu.com/item/%E8%B4%A2%E5%AF%8C/1944587",
        "https://baike.baidu.com/item/%E6%BF%80%E5%8A%B1/13132931",
        "https://baike.baidu.com/item/%E5%8F%98%E9%87%8F/3956968",
        "https://baike.baidu.com/item/%E5%88%9B%E6%96%B0/6047",
        "https://baike.baidu.com/item/%E5%90%88%E4%BC%99%E5%88%B6",
        "https://baike.baidu.com/item/%E5%A4%B1%E4%B8%9A/1167661",
        "https://baike.baidu.com/item/%E9%A2%84%E6%9C%9F",
        "https://baike.baidu.com/item/%E7%BB%8F%E6%B5%8E%E5%AD%A6",
        "https://baike.baidu.com/item/%E6%88%90%E6%9C%AC",
        "https://baike.baidu.com/item/%E5%B9%B3%E5%9D%87%E6%88%90%E6%9C%AC",
        "https://baike.baidu.com/item/%E5%82%A8%E8%93%84",
        "https://baike.baidu.com/item/%E6%9B%BF%E4%BB%A3%E6%95%88%E5%BA%94",
        "https://baike.baidu.com/item/%E5%AE%8C%E5%85%A8%E7%AB%9E%E4%BA%89",
        "https://baike.baidu.com/item/%E5%85%85%E5%88%86%E5%B0%B1%E4%B8%9A",
        "https://baike.baidu.com/item/%E5%AD%98%E6%AC%BE%E5%87%86%E5%A4%87%E9%87%91%E7%8E%87?fromtitle=%E5%87%86%E5%A4%87%E9%87%91%E7%8E%87&fromid=6845081",
        "https://baike.baidu.com/item/%E6%B6%88%E8%B4%B9%E8%80%85%E5%89%A9%E4%BD%99",
        "https://baike.baidu.com/item/%E7%BB%8F%E6%B5%8E%E5%91%A8%E6%9C%9F",
        "https://baike.baidu.com/item/%E9%9C%80%E6%B1%82%E8%A1%A8",
        "https://baike.baidu.com/item/%E5%87%BA%E5%8F%A3/566642",
        "https://baike.baidu.com/item/%E8%B4%A7%E5%B8%81%E5%B8%82%E5%9C%BA",
        "https://baike.baidu.com/item/%E5%A2%9E%E5%80%BC%E7%A8%8E",
        "https://baike.baidu.com/item/%E7%9F%A5%E8%AF%86%E4%BA%A7%E6%9D%83/85044",
        "https://baike.baidu.com/item/%E9%9D%9E%E8%87%AA%E6%84%BF%E6%80%A7%E5%A4%B1%E4%B8%9A?fromtitle=%E9%9D%9E%E8%87%AA%E6%84%BF%E5%A4%B1%E4%B8%9A&fromid=2198212",
        "https://baike.baidu.com/item/%E7%9C%8B%E4%B8%8D%E8%A7%81%E7%9A%84%E6%89%8B/7294754",
        "https://baike.baidu.com/item/%E5%9B%BD%E5%86%85%E7%94%9F%E4%BA%A7%E6%80%BB%E5%80%BC/31864?fromtitle=GDP&fromid=41201",
        "https://baike.baidu.com/item/%E6%AD%A7%E8%A7%86",
        "https://baike.baidu.com/item/%E6%95%88%E7%8E%87",
        "https://baike.baidu.com/item/%E4%BE%9B%E7%BB%99%E6%9B%B2%E7%BA%BF",
        "https://baike.baidu.com/item/%E8%B4%AB%E5%9B%B0",
        "https://baike.baidu.com/item/%E5%80%BA%E5%88%B8",
        "https://baike.baidu.com/item/%E7%A8%80%E7%BC%BA/5226430",
        "https://baike.baidu.com/item/%E5%AE%8F%E8%A7%82%E7%BB%8F%E6%B5%8E%E5%AD%A6/27041",
        "https://baike.baidu.com/item/%E8%B4%A7%E5%B8%81%E5%AD%A6%E6%B4%BE?fromtitle=%E8%B4%A7%E5%B8%81%E4%B8%BB%E4%B9%89&fromid=1826836",
        "https://baike.baidu.com/item/%E5%B9%B3%E7%AD%89",
        "https://baike.baidu.com/item/%E5%85%AC%E6%9C%89%E8%B5%84%E6%BA%90",
        "https://baike.baidu.com/item/%E9%87%91%E8%9E%8D%E5%AD%A6/51188",
        "https://baike.baidu.com/item/%E4%B9%98%E6%95%B0%E6%95%88%E5%BA%94",
        "https://baike.baidu.com/item/%E6%8A%95%E8%B5%84",
        "https://baike.baidu.com/item/%E5%AE%9E%E9%99%85%E5%B7%A5%E8%B5%84",
        "https://baike.baidu.com/item/%E5%A4%B1%E4%B8%9A%E8%80%85",
        "https://baike.baidu.com/item/%E8%9E%8D%E8%B5%84/426146",
        "https://baike.baidu.com/item/%E9%A3%8E%E9%99%A9/2833020",
        "https://baike.baidu.com/item/%E9%AB%98%E5%88%A9%E8%B4%B7/66090",
        "https://baike.baidu.com/item/%E6%97%A0%E8%B0%93%E6%8D%9F%E5%A4%B1",
        "https://baike.baidu.com/item/%E5%A4%B1%E4%B8%9A%E4%BF%9D%E9%99%A9",
        "https://baike.baidu.com/item/%E5%95%86%E4%B8%9A%E9%93%B6%E8%A1%8C",
        "https://baike.baidu.com/item/%E6%9C%89%E5%BD%A2%E8%B5%84%E4%BA%A7",
        "https://baike.baidu.com/item/%E7%94%9F%E4%BA%A7%E8%A6%81%E7%B4%A0",
        "https://baike.baidu.com/item/%E5%9B%BD%E9%99%85%E6%94%B6%E6%94%AF%E5%B9%B3%E8%A1%A1%E8%A1%A8",
        "https://baike.baidu.com/item/%E4%BB%B7%E6%A0%BC%E6%8C%87%E6%95%B0",
        "https://baike.baidu.com/item/%E5%AE%9A%E6%9C%9F%E5%AD%98%E6%AC%BE",
        "https://baike.baidu.com/item/%E4%BB%B7%E6%A0%BC%E6%AD%A7%E8%A7%86",
        "https://baike.baidu.com/item/%E4%BA%BA%E5%9D%87%E5%8F%AF%E6%94%AF%E9%85%8D%E6%94%B6%E5%85%A5/9866975",
        "https://baike.baidu.com/item/%E8%B5%84%E6%BA%90%E9%85%8D%E7%BD%AE",
        "https://baike.baidu.com/item/%E5%9B%9A%E5%BE%92%E5%9B%B0%E5%A2%83",
        "https://baike.baidu.com/item/%E6%80%BB%E4%BE%9B%E7%BB%99",
        "https://baike.baidu.com/item/%E5%A7%94%E6%89%98%E4%BA%BA/29559",
        "https://baike.baidu.com/item/%E5%88%A9%E6%81%AF",
        "https://baike.baidu.com/item/%E7%BB%9D%E5%AF%B9%E4%BC%98%E5%8A%BF",
        "https://baike.baidu.com/item/%E5%B8%82%E5%9C%BA/238002",
        "https://baike.baidu.com/item/%E4%BA%A7%E6%9D%83",
        "https://baike.baidu.com/item/%E4%B8%AA%E4%BA%BA%E6%89%80%E5%BE%97%E7%A8%8E",
        "https://baike.baidu.com/item/%E8%BF%9B%E5%8F%A3",
        "https://baike.baidu.com/item/%E6%8A%95%E5%85%A5",
        "https://baike.baidu.com/item/%E8%A1%A5%E8%B4%B4",
        "https://baike.baidu.com/item/%E9%A2%84%E7%AE%97",
        "https://baike.baidu.com/item/%E9%A2%84%E6%9C%9F%E5%9E%8B%E9%80%9A%E8%B4%A7%E8%86%A8%E8%83%80/7650227",
        "https://baike.baidu.com/item/%E8%A1%B0%E9%80%80",
        "https://baike.baidu.com/item/%E6%8A%80%E6%9C%AF%E8%BF%9B%E6%AD%A5",
        "https://baike.baidu.com/item/%E7%90%86%E6%80%A7%E9%A2%84%E6%9C%9F/698739",
        "https://baike.baidu.com/item/%E6%A8%A1%E5%9E%8B",
        "https://baike.baidu.com/item/%E8%81%94%E9%82%A6%E5%9F%BA%E9%87%91%E5%88%A9%E7%8E%87",
        "https://baike.baidu.com/item/%E5%9B%9E%E6%8A%A5/6346386",
        "https://baike.baidu.com/item/%E8%87%AA%E7%84%B6%E8%B5%84%E6%BA%90",
        "https://baike.baidu.com/item/%E9%95%BF%E6%9C%9F",
        "https://baike.baidu.com/item/%E8%BF%87%E5%89%A9/11055044",
        "https://baike.baidu.com/item/%E5%A4%9A%E5%85%83%E5%8C%96",
        "https://baike.baidu.com/item/%E9%93%B6%E8%A1%8C%E8%B4%A7%E5%B8%81",
        "https://baike.baidu.com/item/%E9%9D%9E%E5%9D%87%E8%A1%A1",
        "https://baike.baidu.com/item/%E5%8B%BE%E7%BB%93",
        "https://baike.baidu.com/item/%E4%B8%AD%E4%BD%8D%E6%95%B0",
        "https://baike.baidu.com/item/%E5%8A%B3%E5%8A%A8%E5%8A%9B",
        "https://baike.baidu.com/item/%E8%B4%A7%E5%B8%81/85299",
        "https://baike.baidu.com/item/%E5%81%9C%E6%BB%9E%E6%80%A7%E9%80%9A%E8%B4%A7%E8%86%A8%E8%83%80/833382?fromtitle=%E6%BB%9E%E8%83%80&fromid=2311884",
        "https://baike.baidu.com/item/%E8%B4%B8%E6%98%93%E5%A3%81%E5%9E%92",
        "https://baike.baidu.com/item/%E5%A5%97%E5%88%A9",
        "https://baike.baidu.com/item/%E8%B4%9F%E6%89%80%E5%BE%97%E7%A8%8E",
        "https://baike.baidu.com/item/%E8%B4%A7%E5%B8%81%E6%B5%81%E9%80%9A%E9%80%9F%E5%BA%A6",
        "https://baike.baidu.com/item/%E8%A7%84%E6%A8%A1%E7%BB%8F%E6%B5%8E",
        "https://baike.baidu.com/item/%E5%B8%82%E5%9C%BA%E7%BB%8F%E6%B5%8E",
        "https://baike.baidu.com/item/%E6%9C%89%E9%99%90%E8%B4%A3%E4%BB%BB",
        "https://baike.baidu.com/item/%E9%80%9A%E8%B4%A7%E8%86%A8%E8%83%80%E7%8E%87",
        "https://baike.baidu.com/item/%E6%80%BB%E9%9C%80%E6%B1%82",
        "https://baike.baidu.com/item/%E5%8D%9A%E5%BC%88%E8%AE%BA/81545",
        "https://baike.baidu.com/item/%E5%8F%AF%E5%8F%98%E6%88%90%E6%9C%AC",
        "https://baike.baidu.com/item/%E7%BE%8E%E5%9B%BD%E8%81%94%E9%82%A6%E5%82%A8%E5%A4%87%E7%B3%BB%E7%BB%9F/2297802",
        "https://baike.baidu.com/item/%E5%85%AC%E5%85%B1%E5%80%BA%E5%8A%A1",
        "https://baike.baidu.com/item/%E9%87%8D%E5%95%86%E4%B8%BB%E4%B9%89",
        "https://baike.baidu.com/item/%E4%BF%9D%E6%8A%A4%E4%B8%BB%E4%B9%89",
        "https://baike.baidu.com/item/%E5%B7%A5%E4%BC%9A",
        "https://baike.baidu.com/item/%E5%8D%87%E5%80%BC",
        "https://baike.baidu.com/item/%E5%B9%B3%E5%9D%87%E6%95%B0?fromtitle=%E5%9D%87%E5%80%BC&fromid=5922988",
        "https://baike.baidu.com/item/%E6%80%BB%E6%88%90%E6%9C%AC",
        "https://baike.baidu.com/item/%E6%9C%80%E4%BD%8E%E6%88%90%E6%9C%AC",
        "https://baike.baidu.com/item/%E4%B8%8D%E5%AE%8C%E5%85%A8%E7%AB%9E%E4%BA%89",
        "https://baike.baidu.com/item/%E7%94%9F%E5%91%BD%E5%91%A8%E6%9C%9F",
        "https://baike.baidu.com/item/%E5%9D%87%E8%A1%A1/10893468",
        "https://baike.baidu.com/item/%E8%B5%84%E4%BA%A7",
        "https://baike.baidu.com/item/%E7%A8%80%E7%BC%BA%E6%80%A7",
        "https://baike.baidu.com/item/%E5%86%85%E5%9C%A8%E4%BB%B7%E5%80%BC",
        "https://baike.baidu.com/item/%E5%A4%96%E6%B1%87",
        "https://baike.baidu.com/item/%E5%9C%9F%E5%9C%B0/12005092",
        "https://baike.baidu.com/item/%E5%85%AC%E5%85%B1%E7%89%A9%E5%93%81",
        "https://baike.baidu.com/item/%E5%90%88%E6%88%90%E8%B0%AC%E8%AF%AF",
    ]
    allowed_domains = ["baike.baidu.com"]
    rules = (
        Rule(LinkExtractor(allow=r'/item/[%a-zA-Z0-9/\?\-\.\=]+$',allow_domains=["baike.baidu.com"],restrict_xpaths="//a[starts-with(@href,'/item/') and not(contains(@href,'_')) and not(contains(@href,'#'))]"),callback='parse_links_and_pages',follow=True,process_links="process_links"),
    )
    #_requests_to_follow(self, response):调用process_Links
    #process_links的目的是不浪费重定向过后页面的链接，将这些链接
    #全部指向baike.baidu.com，而不是wapbaike.com.
    #如果不这样做，后果是解析wapbaike会与baike重复，形成并行的两条线路，效率低
    #解决重定向问题

    def process_links(self ,links):
        for link in links:
            if (link.url[0:23] != 'https://baike.baidu.com'):
                link.url = 'https://baike.baidu.com'+link.url[26:len(link.url)]
        return links


    def parse_start_url(self, response):
        yield Request(response.url,callback=self.parse_links_and_pages)


    def parse_links_and_pages(self,response):
        ##爬取所有文本链接
        #
        if(response.url[0:23] == 'https://baike.baidu.com'):
            self.log('GO to page : ' + response.url, level=logging.INFO)
        ##爬取所有的Page
            try:
                PageItem_loader = BaikePageLoader(BaikePageItem(), response)
                PageItem_loader.add_xpath('topic',"//dd[@class='lemmaWgt-lemmaTitle-title']/h1/text()|//dd[@class='lemmaWgt-lemmaTitle-title']/h2/text()")
                # 去除"https://baike.baidu.com"
                PageItem_loader.add_value('topic_url', response.url[23:])
                PageItem_loader.add_xpath('detail_text',"//div[@class='para']/text()|//div[@class='para']/b/text()|//div[@class='para']/i/text()|//div[@class='para']/a[starts-with(@href,'/item/') and not(contains(@href,'=')) and not(contains(@href,'_')) and not(contains(@href,'#'))]|//h2[@class='title-text']|//h3[@class='title-text']")
                #
                PageItem_loader.add_value('detail_text'," ")
                #
                PageItem = PageItem_loader.load_item()
                yield PageItem
            except Exception as err:
                self.log(response.url+' Go ERROR line ' + str(sys._getframe().f_lineno), level=logging.CRITICAL)

        elif(response.url[0:26] == 'https://wapbaike.baidu.com'):
        ##爬取所有的Page
            try:
                PageItem_loader = BaikePageLoader(BaikePageItem(), response)
                PageItem_loader.add_xpath('topic',"//div[starts-with(@class,'lemma-title-container')]/span[@class='lemma-title']/text()|//h1/text()")
                # 去除"https://wapbaike.baidu.com"
                PageItem_loader.add_value('topic_url', response.url[26:])
                # 如果还有二级描述
                if (len(response.xpath("//li[@class='extra-list-item extra-lemma-desc']"))!=0):
                    PageItem_loader.add_value('topic','（')
                    PageItem_loader.add_xpath('topic', "//li[@class='extra-list-item extra-lemma-desc']/text()")
                    PageItem_loader.add_value('topic', '）')
                PageItem_loader.add_xpath('detail_text',"//div[@class='para']/text()|//div[@class='para']/b/text()|//div[@class='para']/i/text()|//div[@class='para']/a[starts-with(@href,'/item/') and not(contains(@href,'=')) and not(contains(@href,'_')) and not(contains(@href,'#'))]|//h2[@class='title-level-2']/text()|//h3[@class='title-level-3']/text()|//div[starts-with(@class,'summary')]/p/text()|//div[starts-with(@class,'summary')]/p/b/text()|//div[starts-with(@class,'summary')]/p/i/text()|//div[starts-with(@class,'summary')]/p/a[starts-with(@href,'/item/') and not(contains(@href,'=')) and not(contains(@href,'_')) and not(contains(@href,'#'))]")
                #
                PageItem_loader.add_value('detail_text'," ")
                #
                PageItem = PageItem_loader.load_item()
                yield PageItem
            except Exception as err:
                self.log(response.url+' Go ERROR line ' + str(sys._getframe().f_lineno), level=logging.CRITICAL)
        else:
            self.log(response.url +' Mismatched Format',level=logging.CRITICAL)

            #  4004002
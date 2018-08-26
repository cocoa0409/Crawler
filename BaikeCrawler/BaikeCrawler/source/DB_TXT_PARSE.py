# -*-coding: utf8-*-
import traceback
import xml.dom.minidom
from threading import Thread
from xml.dom.minidom import Document
import re
import logging
import os
# 模式更改
import pymysql
import json


def linkandh2h3formatchange_advanced(text):
    link = re.compile(r'<a.+?href.*?/item/.*?</a>')
    text = link.sub(replace_link_advanced, text)
    h2h3 = re.compile(r'<h.+?</h.>')
    text = h2h3.sub(replace_h2h3, text)

    xmlparse = re.compile(r'[><&]')
    text = xmlparse.sub(replace_xml,text)
    return text

def replace_link_advanced(input):
    global cur
    value = input.group()
    text = re.findall(r'>[^\s\n]+?<', value)
    if len(text) == 0:
        text = re.findall(r'>[^\n]+?<', value)
    if len(text) == 0:
        return '\n'
    text = text[0]
    text = text[1:len(text) - 1]
    # 解决加粗文本问题
    if '<b>' in text or '<i>' in text:
        text = text[3:len(text)]

    linkto_url = re.findall(r'/item/[%a-zA-Z0-9/?=.-]+', value)
    if len(linkto_url) == 0:
        logging.log(logging.CRITICAL,"unknown format："+value)
    linkto_url = linkto_url[0]
    result = find_topic_from_url_refinement(linkto_url)
    if result == None:
        try:
            sql = "insert into pageunknown(page_url) VALUES (\'" + linkto_url + "\') on DUPLICATE KEY UPDATE page_url=values(page_url);"
            cur.execute(sql)
        except:
            sql = 'insert into pageunknown(page_url) VALUES (\"' + linkto_url + '\") on DUPLICATE KEY UPDATE page_url=values(page_url);'
            cur.execute(sql)
        #logging.log(logging.CRITICAL,"unfound topic of "+text+' :'+linkto_url)
        result = text
    return '[[' + result + '|' + text + ']]'


def replace_h2h3(input):
    value = input.group()
    text = re.findall('>[^></\s\n]+?</h', value)
    if len(text)==0:
        text = re.findall('>[^></\n]+?</h', value)
    if len(text)==0:
        return '\n'
    text = text[0]
    text = text[1:len(text) - 3]
    return '\n\n' + text + '\n'

def replace_xml(input):
    value = input.group()
    if value == '<':
        return '&lt;'
    elif value == '&':
        return '&amp;'
    elif value == '>':
        return '&gt;'


def get_urlid_complicate2(URL):
    word_set = []
    id_set = []
    # /item/....?force=1
    extractor_force=re.compile(r'/item/.*?\?force=1$')
    temp = extractor_force.findall(URL)
    if len(temp) != 0:
        return word_set,id_set
    # /item/2046
    extractor0 = re.compile(r'^/item/\d*?$')
    temp = extractor0.findall(URL)
    if len(temp) != 0:
        extractor0 = re.compile(r'\d*?$')
        word_set.append(extractor0.findall(URL)[0])
        return word_set, id_set

    extractor1 = re.compile(r'\?fromtitle=.*?$')
    temp = extractor1.findall(URL)
    if len(temp) != 0:
        redirect = temp[0]
        extractor2 = re.compile(r'\?fromtitle=.*?fromid=')
        word = extractor2.findall(redirect)
        word_set.append(word[0][11:len(word[0]) - 8])
        extractor3 = re.compile(r'fromid=.*?$')
        id = extractor3.findall(redirect)
        id_set.append(id[0][7:])
        URL = extractor1.sub('', URL)

    # /item/2046
    extractor0 = re.compile(r'^/item/\d*?$')
    temp = extractor0.findall(URL)
    if len(temp) != 0:
        extractor0 = re.compile(r'\d*?$')
        word_set.append(extractor0.findall(URL)[0])
        return word_set, id_set

    extractor5 = re.compile(r'/\d+?$')
    id = extractor5.findall(URL)

    if len(id) != 0:
        id_set.append(id[0][1:])
        URL = extractor5.sub('', URL)

    extractor6 = re.compile(r'/item/.*?$')
    word = extractor6.findall(URL)
    word_set.append(word[0][6:])
    return word_set, id_set


def find_topic_from_url_refinement(url):
    global cur
    word_set,id_set=get_urlid_complicate2(url)
    if len(id_set) != 0:
        sql="select page_topic from pagesearch where page_urlcode = \'" + word_set[0] + "\' and page_urlid=\'" + id_set[0] +"\';"
        cur.execute(sql)
        topic_set = cur.fetchall()
        if len(topic_set) == 0:
            if len(id_set) == 2:
                sql = "select page_topic from pagesearch where page_urlcode = \'" + word_set[1] + "\' and page_urlid=\'" + id_set[1] + "\';"
                cur.execute(sql)
                topic_set = cur.fetchall()
                if len(topic_set) == 0:
                    return None
                else:
                    return topic_set[0][0]
            else:
                return None
        else:
            return topic_set[0][0]
    else:
        sql="select page_topic from (select * from pagesearch where page_urlcode = \'"+word_set[0]+"\') subtable where page_urlid_int=(select min(page_urlid_int) from (select * from pagesearch where page_urlcode = \'"+word_set[0]+"\') subtable);"
        cur.execute(sql)
        topic_set=cur.fetchall()
        if len(topic_set) == 0:
            return None
        else:
            return topic_set[0][0]




def mysql_makesure_seen_or_not(topic):
    global cur
    try:
        sql="select page_topic from pageremark where page_topic=\'"+topic+"\';"
        result = cur.execute(sql)
    except:
        sql='select page_topic from pageremark where page_topic=\"'+topic+'\";'
        result = cur.execute(sql)

    if result == 1:
        return True
    elif result ==0:
        return False
    else:
        logging.log(logging.ERROR,"unknown response in pageremark mysql:"+str(result))

def WikiFormatChanging(topic, id_int, parentid_int, text):
    id= str(id_int)
    parentid=str(parentid_int)
    xmlparse = re.compile(r'[><&]')
    topic = xmlparse.sub(replace_xml,topic)
    return('<page>\n<title>'+topic+'</title>\n<id>'+id+'</id>\n<parentid>'+parentid+'</parentid>\n<revision>\n<text>'+text+'</text>\n</revision>\n</page>\n')

'''
strat_page:代表JSON文件中行数范围，输入0代表从1行开始
end_page:代表JSON文件中行数范围，输入1000代表到1000行结束
'''

def is_disambiguous(URL):
    extractor_force=re.compile(r'/item/.*?\?force=1$')
    temp = extractor_force.findall(URL)
    if len(temp) != 0:
        return True
    else:
        return False


def read_current_txt_and_add_ranged_page(JSON_path,start_id,target_txt_path):
    with open(target_txt_path, encoding="utf-8", mode="a") as data:
        global cur
        i = start_id
        with open(JSON_path, 'r',encoding='utf-8') as f:
            for dataline in f:
                if i%10000 ==0:
                    logging.critical('TXT_PARSE: go '+ str(i+1) + ' -> ' + str(i +10000))
                JSON = json.loads(dataline)
                #判断是否输出过此页面
                seen_or_not = mysql_makesure_seen_or_not(JSON['topic'])
                is_disambiguous_page = is_disambiguous(JSON['topic_url'])
                if seen_or_not == True or is_disambiguous_page == True:
                    i = i + 1
                    continue
                elif seen_or_not == False:
                    i = i + 1
                    try:
                        #插入新数据
                        data.write(WikiFormatChanging(JSON['topic'], i, 0, linkandh2h3formatchange_advanced(JSON['detail_text'])))
                        try:
                            sql = "insert into pageremark(page_topic,page_sort_index) values (\'" + JSON['topic'] + "\'," + str(i) + ")on DUPLICATE KEY UPDATE page_topic=values(page_topic),page_sort_index=values(page_sort_index);"
                            cur.execute(sql)
                        except:
                            sql = 'insert into pageremark(page_topic,page_sort_index) values (\"' + JSON['topic'] + '\",' + str(i) + ')on DUPLICATE KEY UPDATE page_topic=values(page_topic),page_sort_index=values(page_sort_index);'
                            cur.execute(sql)
                    except:
                        logfile=open('Writing.log','w')
                        traceback.print_exc()
                        traceback.print_exc(file=logfile)
                        logfile.write(JSON['topic']+'          '+str(i)+'\n')
                        logfile.close()
                    con.commit()
    return i

def write_start(target_txt_path):
    with open(target_txt_path, encoding="utf-8", mode="w") as data:
        data.write('<?xml version="1.0" ?>\n<mediawiki version="0.10" xml:lang="zh" xmlns="http://www.mediawiki.org/xml/export-0.10/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.10/ http://www.mediawiki.org/xml/export-0.10.xsd">\n<siteinfo>\n<sitename>Wikipedia</sitename>\n<dbname>zhwiki</dbname>\n<base>https://zh.wikipedia.org/wiki/Wikipedia:%E9%A6%96%E9%A1%B5</base>\n<generator>MediaWiki 1.31.0-wmf.23</generator>\n<case>first-letter</case>\n<namespaces>\n<namespace case="first-letter" key="-2">Media</namespace>\n<namespace case="first-letter" key="-1">Special</namespace>\n<namespace case="first-letter" key="0"/>\n<namespace case="first-letter" key="1">Talk</namespace>\n<namespace case="first-letter" key="2">User</namespace>\n<namespace case="first-letter" key="3">User talk</namespace>\n<namespace case="first-letter" key="4">Wikipedia</namespace>\n<namespace case="first-letter" key="5">Wikipedia talk</namespace>\n<namespace case="first-letter" key="6">File</namespace>\n<namespace case="first-letter" key="7">File talk</namespace>\n<namespace case="first-letter" key="8">MediaWiki</namespace>\n<namespace case="first-letter" key="9">MediaWiki talk</namespace>\n<namespace case="first-letter" key="10">Template</namespace>\n<namespace case="first-letter" key="11">Template talk</namespace>\n<namespace case="first-letter" key="12">Help</namespace>\n<namespace case="first-letter" key="13">Help talk</namespace>\n<namespace case="first-letter" key="14">Category</namespace>\n<namespace case="first-letter" key="15">Category talk</namespace>\n<namespace case="first-letter" key="100">Portal</namespace>\n<namespace case="first-letter" key="101">Portal talk</namespace>\n<namespace case="first-letter" key="118">Draft</namespace>\n<namespace case="first-letter" key="119">Draft talk</namespace>\n<namespace case="first-letter" key="828">模块</namespace>\n<namespace case="first-letter" key="829">模块讨论</namespace>\n<namespace case="first-letter" key="2300">Gadget</namespace>\n<namespace case="first-letter" key="2301">Gadget talk</namespace>\n<namespace case="case-sensitive" key="2302">Gadget definition</namespace>\n<namespace case="case-sensitive" key="2303">Gadget definition talk</namespace>\n<namespace case="first-letter" key="2600">Topic</namespace>\n</namespaces>\n</siteinfo>')


def write_end(target_txt_path):
    with open(target_txt_path, encoding="utf-8", mode="a") as data:
        data.write('</mediawiki>')




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



import time
start = time.clock()

output_path = "/Users/choukichiou/Desktop/BaikeCrawler/output_files/result.txt"

write_start(output_path)

JSON_path="/Users/choukichiou/Desktop/BaikeCrawler/output_files/JSON_P6yfu30M.json"
id_total= read_current_txt_and_add_ranged_page(JSON_path,0 , output_path)
print(id_total)

JSON_path="/Users/choukichiou/Desktop/BaikeCrawler/output_files/JSON_qkXMQlvE.json"
id_total= read_current_txt_and_add_ranged_page(JSON_path, 4000000, output_path)
print(id_total)

JSON_path="/Users/choukichiou/Desktop/BaikeCrawler/output_files/JSON_S6C8NiE1.json"
id_total= read_current_txt_and_add_ranged_page(JSON_path, 8000000, output_path)
write_end(output_path)


con.close()

end = time.clock()
print(end - start)
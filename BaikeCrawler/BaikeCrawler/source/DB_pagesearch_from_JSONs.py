import pymysql
import json
import logging
import re

def get_urlid_complicate2(URL):
    word_set = []
    id_set = []
    # /item/....?force=1 返回空
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


def DB_pagesearch_from_JSONs(Target_JSON_set):
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

    for JSON_path in Target_JSON_set:
        with open(JSON_path, 'r') as f:
            logging.critical('generating Pagesearch: '+JSON_path)
            i = 0
            for dataline in f:
                JSON = json.loads(dataline)
                if i % 10000 == 0:
                    con.commit()
                    logging.critical(' get pagesearch from JSON files : go ' + str(i + 1) + ' -> ' + str(i + 10000))
                topic = JSON['topic']
                url = JSON['topic_url']
                word_set, id_set = get_urlid_complicate2(url)
                if len(id_set) == 0 and len(word_set) != 0:
                    try:
                        input_sql = "insert into pagesearch(page_topic,page_urlcode,page_urlid,page_urlid_int) values (\'" + topic + "\',\'" + word_set[0] + "\',\'0\',0)on DUPLICATE KEY UPDATE page_topic=values(page_topic),page_urlcode=values(page_urlcode),page_urlid=values(page_urlid);"
                        cur.execute(input_sql)
                    except:
                        input_sql = 'insert into pagesearch(page_topic,page_urlcode,page_urlid,page_urlid_int) values (\"' + topic + '\",\"' + word_set[0] + '\",\"0\",0)on DUPLICATE KEY UPDATE page_topic=values(page_topic),page_urlcode=values(page_urlcode),page_urlid=values(page_urlid);'
                        cur.execute(input_sql)

                else:
                    if len(word_set) != len(id_set):
                        try:
                            input_sql = "insert into pagesearch(page_topic,page_urlcode,page_urlid,page_urlid_int) values (\'" + topic + "\',\'" + word_set[1] + "\',\'0\',0)on DUPLICATE KEY UPDATE page_topic=values(page_topic),page_urlcode=values(page_urlcode),page_urlid=values(page_urlid);"
                            cur.execute(input_sql)
                        except:
                            input_sql = 'insert into pagesearch(page_topic,page_urlcode,page_urlid,page_urlid_int) values (\"' + topic + '\",\"' + word_set[1] + '\",\"0\",0)on DUPLICATE KEY UPDATE page_topic=values(page_topic),page_urlcode=values(page_urlcode),page_urlid=values(page_urlid);'
                            cur.execute(input_sql)
                    for num in range(0, len(id_set)):
                        try:
                            input_sql = "insert into pagesearch(page_topic,page_urlcode,page_urlid,page_urlid_int) values (\'" + topic + "\',\'" + word_set[num] + "\',\'" + id_set[num] + "\'," + id_set[num] + ")on DUPLICATE KEY UPDATE page_topic=values(page_topic),page_urlcode=values(page_urlcode),page_urlid=values(page_urlid);"
                            cur.execute(input_sql)
                        except:
                            input_sql = 'insert into pagesearch(page_topic,page_urlcode,page_urlid,page_urlid_int) values (\"' + topic + '\",\"' + word_set[num] + '\",\"' + id_set[num] + '\",' + id_set[num] + ')on DUPLICATE KEY UPDATE page_topic=values(page_topic),page_urlcode=values(page_urlcode),page_urlid=values(page_urlid);'
                            cur.execute(input_sql)
    con.commit()
    con.close()



Target_JSON_set = []
Target_JSON_set.append("/Users/choukichiou/Desktop/BaikeCrawler/output_files/JSON_qkXMQlvE.json")
Target_JSON_set.append("/Users/choukichiou/Desktop/BaikeCrawler/output_files/JSON_S6C8NiE1.json")
##.....
DB_pagesearch_from_JSONs(Target_JSON_set)
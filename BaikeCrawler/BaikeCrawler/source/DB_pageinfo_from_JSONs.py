import pymysql
import json
import logging

def DB_pageinfo_from_JSONs(Target_JSON_set):
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
            logging.critical('generating pageinfo: ' + JSON_path)
            i = 0
            for dataline in f:
                JSON = json.loads(dataline)
                if i % 10000 == 0:
                    con.commit()
                    logging.critical('generating pageinfo: go ' + str(i + 1) + ' -> ' + str(i + 10000))
                try:
                    sql = "insert into pageinfo(page_topic,page_url) VALUES (\'" + JSON['topic'] + "\',\'" + JSON['topic_url'] + "\') on DUPLICATE KEY UPDATE page_url=values(page_url),page_topic=values(page_topic);"
                    cur.execute(sql)
                except:
                    sql = 'insert into pageinfo(page_topic,page_url) VALUES (\"' + JSON['topic'] + '\",\"' + JSON['topic_url'] + '\") on DUPLICATE KEY UPDATE page_url=values(page_url),page_topic=values(page_topic);'
                    cur.execute(sql)
                i = i + 1
    con.commit()
    con.close()


Target_JSON_set = []
Target_JSON_set.append("/Users/choukichiou/Desktop/BaikeCrawler/output_files/JSON_qkXMQlvE.json")
Target_JSON_set.append("/Users/choukichiou/Desktop/BaikeCrawler/output_files/JSON_S6C8NiE1.json")
##.....
DB_pageinfo_from_JSONs(Target_JSON_set)
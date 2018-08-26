
import pymysql
import re
import urllib

def joinurl(value):
    return urllib.request.urljoin(
                "https://baike.baidu.com/item/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%A7%91%E5%AD%A6/9132", value)


def changeLinkformat(value):
    #改造链接形式
    if '<a' in value and '</a>' in value:
        text = re.findall('>[^\s\n]+?<', value)[0]
        text = text[1:len(text) - 1]
        linkto_url=re.findall('/item/[%A-Z0-9/]+',value)[0]
        #解决加粗文本问题
        if '<b>' in text:
            text=text[3:len(text)]
        return '[['+linkto_url+'|'+text+']]'
    #改造h2 h3 的 title形式
    elif '<h' in value and '</h' in value:
        text=re.findall('>[^></\s\n]+?</h',value)[0]
        text=text[1:len(text)-3]
        return '\n'+text+'\n'
    else:
        return value

def get_start_urls_from_unknown_links():
    unknown_urls = []
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
    select_sql = 'select page_url from pageunknown;'
    cur.execute(select_sql)
    while True:
        row = cur.fetchone()
        if not row:
            break
        else:
            unknown_url = 'https://baike.baidu.com'+row[0]
            unknown_urls.append(unknown_url)
    return unknown_urls



def unknown_existence():
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
    # 数据库连接
    con2 = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=charset, port=port)
    # 数据库游标
    cur = con.cursor()
    cur2 = con2.cursor()
    select_sql = 'select page_url from pageunknown;'
    cur.execute(select_sql)
    while True:
        row = cur.fetchone()
        if not row:
            break
        else:
            try:
                sql="select * from pageinfo where page_url = \'"+row[0]+"\';"
                result=cur2.execute(sql)
            except:
                sql='select * from pageinfo where page_url = \"'+row[0]+'\";'
                result=cur2.execute(sql)
            if result != 0:
                print(row[0])
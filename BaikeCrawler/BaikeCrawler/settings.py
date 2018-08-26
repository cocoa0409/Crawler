# -*- coding: utf-8 -*-

# Scrapy settings for BaikeCrawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'BaikeCrawler'

SPIDER_MODULES = ['BaikeCrawler.spiders']
NEWSPIDER_MODULE = 'BaikeCrawler.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'BaikeCrawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
# 爬取百科报错 需要设定为 False
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'BaikeCrawler.middlewares.BaikecrawlerSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
#    'BaikeCrawler.middlewares.BaikecrawlerDownloaderMiddleware': 543,
    'BaikeCrawler.middlewares.UserAgentMiddleware' : 400
}


# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    #'BaikeCrawler.pipelines.RedisRecordPipeline':300,
    'BaikeCrawler.pipelines.MySqlRecordPipeline': 500,
    'BaikeCrawler.pipelines.JSONLineExportPipeline': 600,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'




#打log的最低级别 分别是 CRITICAL ERROR WARNING INFO DEBUG
LOG_LEVEL = "DEBUG"
LOG_ENABLED = True
#LOG_FILE = "Baike.log"
LOG_STDOUT = False
LOG_ENCONDING = 'utf-8'

#管理深度优先、广度优先
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'

#管理最大深度
DEPTH_LIMIT=200

#管理 scrapy crawl bk -o item.json 中文输出，否则是unicode编码
FEED_EXPORT_ENCODING = 'utf-8'

#禁止了cookies 提高性能
COOKIES_ENABLED = False
#禁止了重试
RETRY_ENABLED = True
#下载15s就算timeout
DOWNLOAD_TIMEOUT = 15

#关掉重定向?不会重定向到新的地址
REDIRECT_ENABLED = True
#返回302时,按正常返回对待
HTTPERROR_ALLOWED_CODES = [302]

#wapbaike 和 baike的title格式不一致，网址也不一致～～～～～～～～～～～～～～～～～～～～～～待处理
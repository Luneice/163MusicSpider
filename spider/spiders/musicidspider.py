# -*- coding: utf-8 -*-
import scrapy
import re
from selenium import webdriver
import time
import redis
import spider.items as dic
# import json
# from scrapy.selector import Selector
# from scrapy.http import  Request
# from scrapy.spiders import CrawlSpider
# from scrapy.loader import ItemLoader
# from scrapy.linkextractors.sgml import SgmlLinkExtractor


class MusicSpider(scrapy.spiders.Spider):
    name = "musicid"
    allowed_domains = ["163.com"]
    start_urls = [
        "http://music.163.com",
        # "http://music.163.com/#/song?id=108886"
    ]

    browser = webdriver.PhantomJS()

    def __init__(self, category=None, *args, **kwargs):
        super(MusicSpider, self).__init__(*args, **kwargs)
        self.redis_db = redis.Redis(host="localhost", port=6379, db=1)

    def parse(self, response):
        url = "http://music.163.com/#/search/m/"
        self.browser.get(url)
        self.browser.switch_to.frame("g_iframe")
        search_ipt = self.browser.find_element_by_id("m-search-input")
        search_ipt.send_keys(u"邓紫棋")
        search_btn = self.browser.execute_script('return document.querySelector("a.btn.j-flag")')
        search_btn.click()
        time.sleep(5)
        html = self.browser.page_source
        self.parse_music_id(html)
        self.browser.close()

    def parse_music_id(self, html):
        urls = re.findall('<a href="\/song\?id=(.*?)">', html)
        url_set = set(urls)
        for url in url_set:
            print url
            self.redis_db.lpush("url", url)

    def put_url_to_redis(self, urls):
        for url in urls:
            self.redis_db.flushdb()
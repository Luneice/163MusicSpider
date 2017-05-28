# -*- coding: utf-8 -*-
import scrapy
import re
from selenium import webdriver
import spider.items as dic
import time
import redis
# import json
# from scrapy.selector import Selector
# from scrapy.http import  Request
# from scrapy.spiders import CrawlSpider
# from scrapy.loader import ItemLoader
# from scrapy.linkextractors.sgml import SgmlLinkExtractor


class MusicSpider(scrapy.spiders.Spider):
    name = "music"
    allowed_domains = ["163.com"]
    start_urls = [
        "http://music.163.com",
    ]

    def __init__(self, category=None, *args, **kwargs):
        super(MusicSpider, self).__init__(*args, **kwargs)
        self.browser = webdriver.PhantomJS()
        self.file_obj = file

    def __del__(self):
        pass

    def parse(self, response):
        redis_db = redis.Redis(host="localhost", port=6379, db=1)
        while redis_db.keys("url"):
            id = redis_db.lpop("url")
            self.extract_song(id)
        # 关闭浏览器
        print "redis_db已经爬取完了"
        self.browser.close()
        pass

    """
    提取单首歌
    """

    def extract_song(self, musicid):
        url = "http://music.163.com/#/song?id=" + str(musicid)
        self.browser.get(url)
        self.browser.switch_to.frame("g_iframe")
        self.browser.find_element_by_xpath('//*[@id="flag_ctrl"]').click()  # 加载更多的歌词
        next_page = self.browser.find_element_by_class_name("znxt")  # js-disabled
        # 提取音乐的评论信息
        self.parse_musicinfo(self.browser)
        page_no = 0
        while (re.findall("js-disabled", next_page.get_attribute("class")) == []) and page_no < 10:
            self.parse_userinfo(self.browser)
            next_page.click()  # 下一页
            next_page = self.browser.find_element_by_class_name("znxt")  # js-disabled
            page_no += 1
            print "处理了", page_no, "个页面"
        # 关闭文件
        self.file_obj.close()


    def parse_musicinfo(self, browser):
        music_info = dic.MusicInfo()
        music_info['song'] = browser.execute_script('return document.querySelector("em.f-ff2")').text  # 获取歌曲名称
        music_info['singer'] = browser.execute_script('return document.querySelector("p span a.s-fc7")').text  # 获取歌手的名字
        # music_info['special'] = browser.execute_script('return document.querySelector("p a.s-fc7")').text  # 获取专辑
        music_info['lyric'] = browser.find_element_by_id("lyric-content").text
        music_info['dis_num'] = browser.execute_script('return document.querySelector("span#cnt_comment_count")').text  # 获取歌曲的评论量
        self.file_obj = open("Musicinfo/" + music_info['song'] + '-' + music_info['singer'] + ".txt", "w")
        self.file_obj.write("#*歌曲名*#\t" + music_info['song'].encode('utf8') + "\n\n")
        self.file_obj.write("#*歌手名*#\t" + music_info['singer'].encode('utf8') + "\n\n")
        self.file_obj.write("#*评论量*#\t" + music_info['dis_num'].encode('utf8') + "\n\n")
        self.file_obj.write("#*歌词*#\n" + music_info['lyric'].encode('utf8') + "\n\n\n\n")

    def parse_userinfo(self, browser):
        div_list = browser.find_elements_by_class_name("itm")
        for item in div_list:
            user_info = dic.UserInfo()
            user_info["name"] = item.find_element_by_class_name("s-fc7").text
            user_info["dis"] = item.find_element_by_class_name("f-brk").text
            user_info["time"] = item.find_element_by_class_name("s-fc4").text
            user_info["like_num"] = item.find_element_by_css_selector("a[data-type]").text
            self.file_obj.write("#*用户名*#\t" + user_info["name"].encode('utf8') + "\n")
            self.file_obj.write("#*点赞量*#\t" + user_info["like_num"].encode('utf8') + "\n")
            self.file_obj.write("#*留言日期*#\t" + user_info["time"].encode('utf8') + "\n")
            self.file_obj.write("#*留言内容*#\n" + user_info["dis"].encode('utf8') + "\n\n\n\n")

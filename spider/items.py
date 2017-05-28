# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class MusicId(scrapy.Item):
    id = scrapy.Field()

# 歌曲包含的信息
class MusicInfo(scrapy.Item):
    song = scrapy.Field()
    singer = scrapy.Field()
    special = scrapy.Field()
    lyric = scrapy.Field()
    dis_num = scrapy.Field()

# 用户评论信息
class UserInfo(scrapy.Item):
    name = scrapy.Field()
    time = scrapy.Field()
    dis = scrapy.Field()
    # reply = scrapy.Field()
    like_num = scrapy.Field()
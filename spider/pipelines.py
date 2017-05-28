# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class SpiderPipeline(object):
    def process_item(self, item, spider):
        print "管道在处理"
        return item


class MusicIdPipeline(object):
    def __init__(self):
        # self.file = open('items.jl', 'wb')
        print "管道初始化"
        pass

    def process_item(self, item, spider):
        # line = json.dumps(dict(item)) + "\n"
        # self.file.write(line)
        if spider.name == 'musicid':
            print "musicid管道正在工作"
        return item
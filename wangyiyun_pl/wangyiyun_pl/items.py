# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WangyiyunPlItem(scrapy.Item):
    song_id = scrapy.Field()
    user_name = scrapy.Field()
    content = scrapy.Field()
    user_id = scrapy.Field()
    zan_counts = scrapy.Field()
    create_time = scrapy.Field()
    user_img = scrapy.Field()
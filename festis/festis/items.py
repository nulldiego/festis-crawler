# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FestisItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    description = scrapy.Field()
    entry_image = scrapy.Field()
    location = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    category_url = scrapy.Field()
    entry_date = scrapy.Field()
    entry_title = scrapy.Field()
    twitter = scrapy.Field()
    facebook = scrapy.Field()
    web = scrapy.Field()
    url = scrapy.Field()
    geolocation = scrapy.Field()
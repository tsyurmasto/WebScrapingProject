# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlesItem(scrapy.Item):
    # define the fields for your item here like:    
    Title = scrapy.Field()
    Authors = scrapy.Field()
    Year = scrapy.Field()
    Volume = scrapy.Field()
    Pdf_url = scrapy.Field()
    Abstract = scrapy.Field()
    Journal_Conference = scrapy.Field()

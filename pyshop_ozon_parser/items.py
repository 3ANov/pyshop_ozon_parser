# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OzonSmartphoneItem(scrapy.Item):
    """ Item for saving data about smartphone """
    phone_name = scrapy.Field()
    url = scrapy.Field()
    os_name = scrapy.Field()


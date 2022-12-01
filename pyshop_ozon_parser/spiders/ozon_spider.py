import logging as log

import scrapy
from scrapy_selenium import SeleniumRequest

from pyshop_ozon_parser.items import OzonSmartphoneItem


class OzonSpider(scrapy.Spider):
    name = 'ozon_spider'
    allowed_domains = ['www.ozon.ru']

    def start_requests(self):
        url = 'https://www.ozon.ru/category/smartfony-15502/?page=1&sorting=rating'
        yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        log.info(response.url)
        for phones in response.css('div.k5u'):
            item = OzonSmartphoneItem()
            item.name = phones.css('a[href*=tile-hover-target.ok9]::text')[0].extract()
            print(phones.css('a[href*=tile-hover-target.ok9]::text'))

            # print('Проверка ' + phones.css('tile-hover-target ok9'))
            # yield {
            #     'text': phones.css('span.d3z.z3d.d4z.d6z.tsBodyL.ok9').get(),
            # }




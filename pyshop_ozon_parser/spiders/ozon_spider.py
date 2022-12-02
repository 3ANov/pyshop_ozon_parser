import logging as log

import scrapy
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By

from pyshop_ozon_parser.items import OzonSmartphoneItem


class OzonSpider(scrapy.Spider):
    name = 'ozon_spider'
    allowed_domains = ['www.ozon.ru']

    def start_requests(self):
        url = 'https://www.ozon.ru/category/smartfony-15502/?page=1&sorting=rating'
        yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        log.info(response.url)
        # sel = Selector(response)
        driver = response.meta['driver']

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.implicitly_wait(5)
        driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
        phones = driver.find_elements(By.CSS_SELECTOR, '.tile-hover-target')
        # phones = sel.xpath('//a[@class="tile-hover-target kn7"]')
        log.info(phones)
        log.info(len(phones))

        for phone in phones:
            item = OzonSmartphoneItem()
            item['url'] = phone.get_attribute('href')

            # print('Проверка ' + phones.css('tile-hover-target ok9'))
            # yield {
            #     'text': phones.css('span.d3z.z3d.d4z.d6z.tsBodyL.ok9').get(),
            # }
        # yield SeleniumRequest(
        #     url=self.start_urls,
        #     wait_time=1000,
        #     callback=self.parse,
        # )
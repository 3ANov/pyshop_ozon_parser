import logging as log
import scrapy
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from pyshop_ozon_parser.items import OzonSmartphoneItem
from pyshop_ozon_parser.services import SeleniumUndetectedRequest


class OzonSpider(scrapy.Spider):
    name = 'ozon_spider'
    allowed_domains = ['www.ozon.ru']

    # custom_settings = {
    #     'DOWNLOAD_DELAY': 0.5
    # }

    def start_requests(self):
        url = 'https://www.ozon.ru/category/smartfony-15502/?page=1&sorting=rating'
        yield SeleniumUndetectedRequest(url=url, callback=self.parse)

    def parse(self, response):
        log.info(response.url)
        driver = response.meta['driver']
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        phones = []
        while len(phones) < 30:
            phones = list(set(list(map(lambda x: x.get_attribute('href'),
                                       driver.find_elements(By.CSS_SELECTOR, '.tile-hover-target')))))

        driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
        # phones = sel.xpath('//a[@class="tile-hover-target kn7"]')
        # log.info(phones)
        # log.info(len(phones))

        for phone in phones:
            item = OzonSmartphoneItem()
            item['url'] = phone
            # print(item['url'])
            # print(phone)
            yield SeleniumUndetectedRequest(url=item['url'], callback=self.parse_phone_info)
            # print('Проверка ' + phones.css('tile-hover-target ok9'))
            # yield {
            #     'text': phones.css('span.d3z.z3d.d4z.d6z.tsBodyL.ok9').get(),
            # }
        # yield SeleniumRequest(
        #     url=self.start_urls,
        #     wait_time=1000,
        #     callback=self.parse,
        # )

    def parse_phone_info(self, response):
        sel = Selector(response)
        print(response)
        log.info(response.url)
        print(sel.xpath('//a[contains(@href, "section-description--offset-140")]').get())
        # print(sel.xpath('//a[href = "#section-description--offset-140"]').extract())

        # print(sel.css('div#section-characteristics::text').extract())
        # print(sel.xpath('//div[@id="section-characteristics"]').

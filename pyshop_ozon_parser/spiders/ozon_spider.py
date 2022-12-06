import logging as log
import scrapy
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyshop_ozon_parser.items import OzonSmartphoneItem
from pyshop_ozon_parser.services import SeleniumUndetectedRequest


class OzonSpider(scrapy.Spider):
    name = 'ozon_spider'
    allowed_domains = ['www.ozon.ru']

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
            # print(item['url'])
            # print(phone)
            yield SeleniumUndetectedRequest(url=phone, callback=self.parse_phone_info)
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

        driver = response.meta['driver']
        # log.info(response.url)

        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[contains(@data-widget, "webProductHeading")]')),
            message='Ошибка загрузки названия телефона'
        )
        # log.info(element.text)
        # log.info(driver.current_url)

        link_to_description = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "section-description--offset-140")]')),
            message='Ошибка загрузки ссылки на характеристики'
        )

        ActionChains(driver).move_to_element(link_to_description).click(link_to_description).perform()
        yield OzonSmartphoneItem(phone_name=element.text, url=driver.current_url, os_name='')

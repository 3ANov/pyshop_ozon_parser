import itertools
import logging as log
from urllib.request import Request

import scrapy
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyshop_ozon_parser.items import OzonSmartphoneItem
from pyshop_ozon_parser.services import SeleniumUndetectedRequest
from pyshop_ozon_parser.utils import ozon_api_url_creator


class OzonSpider(scrapy.Spider):
    name = 'ozon_spider'
    allowed_domains = ['www.ozon.ru']
    min_number_phones_per_page = 30
    total_count_of_phones = 5
    current_page_of_phones = 1
    phones_dict = {}
    template_page_of_phones_url = 'https://www.ozon.ru/category/smartfony-15502/?page={}&sorting=rating'

    def start_requests(self):

        yield SeleniumUndetectedRequest(url=self.template_page_of_phones_url.format(self.current_page_of_phones),
                                        callback=self.parse_page_of_phones)

    def parse_page_of_phones(self, response):
        log.info(response.url)
        driver = response.meta['driver']
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        phones = []

        while self.min_number_phones_per_page > len(phones):
            phones.extend(driver.find_elements(By.XPATH, '//a[contains(@class, "tile-hover-target")]/span/span'))

        driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
        for phone in phones:
            self.phones_dict[
                phone.find_element(By.XPATH, "./..").find_element(By.XPATH, "./..").get_attribute('href')] = phone.text
        self.phones_dict = dict(itertools.islice(self.phones_dict.items(), 0, self.total_count_of_phones))
        if len(self.phones_dict) < self.total_count_of_phones:
            self.current_page_of_phones += 1
            yield SeleniumUndetectedRequest(url=self.template_page_of_phones_url.format(self.current_page_of_phones),
                                            callback=self.parse_page_of_phones)
        else:
            for phone_url, phone_name in self.phones_dict.items():
                yield SeleniumUndetectedRequest(url=phone_url, callback=self.parse_phone_info,
                                                meta={'phone_url': phone_url, 'phone_name': phone_name})

    def parse_phone_info(self, response):
        driver = response.meta['driver']
        # try:
        log.info(response.request.url)
        log.info(Request(url=ozon_api_url_creator(response.request.url)))
        # link_to_description = WebDriverWait(driver, 10).until(
        #     EC.visibility_of_element_located((By.XPATH, '//a[contains(@href, "section-description--offset-140")]')),
        #     message='Ошибка загрузки ссылки на характеристики'
        # )
        # # raise TimeoutException
        #
        # ActionChains(driver).move_to_element(link_to_description).click(link_to_description).perform()
        driver.execute_script("window.scrollTo(0, 3700);")
        os_name = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Операционная система')]/following::dd/a"))).text

        log.info(os_name)

        # os_name = driver.find_element(By.XPATH, "//span[contains(@text, 'Операционная система')]/following::dd/a/text)]")

        os_version = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//span[contains(text(), 'Версия {os_name}')]/following::dd/a[contains(text(), '{os_name}')]"))).text

        log.info(os_version)


            # os_
        # except TimeoutException:
        #     driver.delete_all_cookies()
        #     yield SeleniumUndetectedRequest(url=response.request.url, callback=self.parse_phone_info,
        #                                     meta={'phone_url': response.meta['phone_url'], 'phone_name': response.meta['phone_name']})

        yield OzonSmartphoneItem(phone_name=response.meta['phone_name'], url=response.meta['phone_url'], os_name=os_name, os_version=os_version)

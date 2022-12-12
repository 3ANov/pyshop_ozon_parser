import itertools
import scrapy
from selenium.webdriver.common.by import By
from pyshop_ozon_parser.items import OzonSmartphoneItem
from pyshop_ozon_parser.services import SeleniumUndetectedRequest
from pyshop_ozon_parser.utils import ozon_api_url_creator, parse_json_find_os_info


class OzonSpider(scrapy.Spider):
    name = 'ozon_spider'
    allowed_domains = ['www.ozon.ru']
    min_number_phones_per_page = 30
    total_count_of_phones = 100
    current_page_of_phones = 1
    phones_dict = {}
    template_page_of_phones_url = 'https://www.ozon.ru/category/smartfony-15502/?page={}&sorting=rating'

    def start_requests(self):

        yield SeleniumUndetectedRequest(url=self.template_page_of_phones_url.format(self.current_page_of_phones),
                                        callback=self.parse_page_of_phones)

    def parse_page_of_phones(self, response):
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
                yield SeleniumUndetectedRequest(url=ozon_api_url_creator(phone_url), callback=self.parse_phone_info,
                                                meta={'phone_url': phone_url, 'phone_name': phone_name})

    def parse_phone_info(self, response):
        os_info = parse_json_find_os_info(response.xpath('//pre/text()').get())
        yield OzonSmartphoneItem(phone_name=response.meta['phone_name'], url=response.meta['phone_url'], os_name=os_info['os_name'], os_version=os_info['os_version'])

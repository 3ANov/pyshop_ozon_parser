import scrapy
from scrapy_selenium import SeleniumRequest


class OzonSpiderSpider(scrapy.Spider):
    name = 'ozon_spider'
    allowed_domains = ['www.ozon.ru']

    def start_requests(self):
        url = 'https://www.ozon.ru/category/smartfony-15502/?page=1&sorting=rating'
        yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        for phones in response.css('div.k5u'):
            print(phones.css('tile-hover-target ok9').get())
            # yield {
            #     'text': phones.css('span.d3z.z3d.d4z.d6z.tsBodyL.ok9').get(),
            # }



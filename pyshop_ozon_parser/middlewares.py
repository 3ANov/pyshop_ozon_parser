# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium.webdriver.support.ui import WebDriverWait
from .services import SeleniumUndetectedRequest
from pyshop_ozon_parser import settings
import undetected_chromedriver as uc
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class SeleniumUndetectedMiddleware:
    """Scrapy middleware handling the requests using selenium"""
    driver_path = settings.UNDETECTED_CHROMEDRIVER_PATH
    options = uc.ChromeOptions()
    options.headless = True
    chrome_prefs = {}

    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"
    options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
    driver = uc.Chrome(options=options, use_subprocess=True, driver_executable_path=driver_path, desired_capabilities=caps)

    def process_request(self, request, spider):
        """Process a request using the selenium driver if applicable"""

        if not isinstance(request, SeleniumUndetectedRequest):
            return None

        self.driver.get(request.url)

        if request.wait_until:
            WebDriverWait(self.driver, request.wait_time).until(
                request.wait_until
            )

        if request.screenshot:
            request.meta['screenshot'] = self.driver.get_screenshot_as_png()

        if request.script:
            self.driver.execute_script(request.script)

        body = str.encode(self.driver.page_source)

        # Expose the driver via the "meta" attribute
        request.meta.update({'driver': self.driver})

        return HtmlResponse(
            self.driver.current_url,
            body=body,
            encoding='utf-8',
            request=request
        )

    def spider_closed(self):
        """Shutdown the driver when spider is closed"""

        self.driver.quit()
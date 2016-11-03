from scrapy.item import Field, Item
import scrapy
from selenium import webdriver
from scrapy.selector import Selector
import time


class GebizItem(Item):
    companyName = Field()
    companyAddress = Field()
    companyPhone = Field()
    product = Field()


class GbizSpider(scrapy.Spider):
    name = "gebiz"
    allowed_domains = ["gebiz.gov.sg"]
    start_urls = [
        'https://www.gebiz.gov.sg/ptn/supplier/directory/index.xhtml',
    ]

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1600, 1000)

    def parse(self, response):
        self.driver.get(response.url)
        self.driver.find_element_by_xpath(".//*[@id='contentForm:search']").click()
        time.sleep(2)
        for count in xrange(2, 832):
            self.driver.find_element_by_xpath(
                ".//*[@id='contentForm:j_idt104:j_idt116_Next_" + str(count) + "']").click()
            time.sleep(2)
            self.html = self.driver.page_source
            self.scraping()

        self.driver.quit()

    def scraping(self):
        for i in range(0, 10):
            time.sleep(2)
            try:
                companyName = Selector(text=self.html).xpath(".//*[@class='commandLink_TITLE-BLUE']/text()").extract()
                name = companyName[i].strip() if companyName else ''
                companyPhone = Selector(text=self.html).xpath(
                    ".//*/tbody/tr/td/div/div/span/table/tbody/tr/td[2]/text()").extract()
                phone = companyPhone[i].strip() if companyPhone else ''
                with open('sg-company.txt', 'a') as f:
                    f.write('{0};{1}\n'.format(name,
                                               phone))
                try:
                    self.driver.find_element_by_name("j_idt117:j_idt119_countdownAlert_OK-BUTTON").click()
                except:
                    pass
            except:
                pass

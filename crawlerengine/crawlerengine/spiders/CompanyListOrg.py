from scrapy.selector import Selector
from scrapy.item import Field, Item
from scrapy.http import Request
import scrapy


class MalayItem(Item):
    companyName = Field()
    companyAddress = Field()
    companyPhone = Field()
    category = Field()


class MalaySpider(scrapy.Spider):
    name = "malaycompany"
    allowed_domains = ["companylist.org"]
    start_urls = [
        'https://companylist.org/Malaysia/',
    ]

    def parse(self, response):
        for i in range(1, 47):
            crawlUrl = response.url + str(i)+".html"
            yield Request(url=crawlUrl, callback=self.parse_pagination, dont_filter=True)

    def parse_pagination(self, response):
        url = Selector(response)
        for i in range(0,35):
            companyName = url.xpath(".//*[@id='content']/div/div[1]/div[4]/div/span/span[1]/a[1]/text()").extract()
            companyName = companyName[i].strip() if companyName else ''
            companyAddress = url.xpath(".//*[@id='content']/div/div[1]/div[4]/div/span/em/span/text()").extract()
            companyAddress = companyAddress[i].strip() if companyAddress else ''
            companyPhone = 'phone'
            category = url.xpath(".//*[@id='content']/div/div[1]/div[4]/div/span/span[2]/a/text()").extract()
            category = category[i].strip() if category  else ''
            item = MalayItem(category=category,
                                  companyName=companyName,
                                  companyAddress=companyAddress,
                                  companyPhone=companyPhone)

            with open('malay-company.txt', 'a') as f:
                f.write('{0};{1};{2};{3}\n'.format(item['category'],
                                                   item['companyName'],
                                                   item['companyAddress'],
                                                   item['companyPhone']))

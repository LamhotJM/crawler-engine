from scrapy.selector import Selector
from scrapy.item import Field, Item
from scrapy.http import Request
import scrapy


class KemenperinItem(Item):
    companyName = Field()
    companyAddress = Field()
    companyPhone = Field()
    product = Field()


class KemenperinSpider(scrapy.Spider):
    name = "idcompany"
    allowed_domains = ["kemenperin.go.id"]
    start_urls = [
        'http://www.kemenperin.go.id/direktori-perusahaan',
    ]

    def parse(self, response):
        for i in range(1, 490):
            crawlUrl = response.url + "?what=&prov=&hal=" + str(i)
            yield Request(url=crawlUrl, callback=self.parse_pagination, dont_filter=True)

    def parse_pagination(self, response):
        url = Selector(response)
        for i in range(0, 50):
            companyName = url.xpath(".//*[@id='newspaper-a']/tbody/tr/td[2]/b/text()").extract()
            companyName = companyName[i].strip() if companyName else ''
            companyAddress = url.xpath(".//*[@id='newspaper-a']/tbody/tr/td[2]/text()[1]").extract()
            companyAddress = companyAddress[i].strip() if companyAddress else ''
            companyPhone = url.xpath(".//*[@id='newspaper-a']/tbody/tr/td[2]/text()[2]").extract()
            companyPhone = companyPhone[i].strip() if companyPhone else ''
            product = url.xpath(".//*[@id='newspaper-a']/tbody/tr/td[3]/text()").extract()
            product = product[i].strip() if product  else ''
            item = KemenperinItem(product=product,
                                  companyName=companyName,
                                  companyAddress=companyAddress,
                                  companyPhone=companyPhone)

            with open('indonesia-company.txt', 'a') as f:
                f.write('{0};{1};{2};{3}\n'.format(item['product'],
                                                   item['companyName'],
                                                   item['companyAddress'],
                                                   item['companyPhone']))

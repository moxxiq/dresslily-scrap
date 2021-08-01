import scrapy


class ManHoodieSpider(scrapy.Spider):
    name = 'man_hoodie'
    allowed_domains = ['https://www.dresslily.com/hoodies-c-181.html']
    start_urls = ['https://www.dresslily.com/hoodies-c-181.html']

    def parse(self, response):
        link_to_product = '//a[contains(@class, "goods-name-link")]/@href'

        for link in response.xpath(link_to_product).extract():
            yield {"url": link}
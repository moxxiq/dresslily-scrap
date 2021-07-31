import scrapy


class ManHoodieSpider(scrapy.Spider):
    name = 'man_hoodie'
    allowed_domains = ['https://www.dresslily.com/hoodies-c-181.html']
    start_urls = ['http://https://www.dresslily.com/hoodies-c-181.html/']

    def parse(self, response):
        pass

import scrapy


class ManHoodieSpider(scrapy.Spider):
    name = 'man_hoodie'
    allowed_domains = ['dresslily.com']
    start_urls = ['https://www.dresslily.com/hoodies-c-181.html']

    def parse(self, response):
        """
        Parse hoodies page. Get all links to the product. Same with rest
        of the pages.
        """
        # XPATH
        link_to_product = '//a[contains(@class, "goods-name-link")]/@href'
        next_page = '//li/a[.="> "]/@href'

        for i, link in enumerate(response.xpath(link_to_product).getall()):
            yield {
                "url": link,
            }

        next_page_url = response.urljoin(response.xpath(next_page).get())
        if next_page_url is not None:
            yield response.follow(next_page_url, callback=self.parse)

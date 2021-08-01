import scrapy
from scrapy_splash import SplashRequest
from re import findall


class ManHoodieSpider(scrapy.Spider):
    name = 'man_hoodie'
    allowed_domains = ['dresslily.com']
    start_urls = ['https://www.dresslily.com/hoodies-c-181.html']

    def parse(self, response):
        """
        Parse men's hoodies page. Get all links to the product. Same with rest
        of the pages.
        """
        # XPATH
        link_to_product = '//a[contains(@class, "goods-name-link")]/@href'
        next_page = '//li/a[.="> "]/@href'

        for link in response.xpath(link_to_product).getall():
            yield SplashRequest(link, self.parse_product_page, args={'wait': 0.5})

        next_page_url = response.urljoin(response.xpath(next_page).get())
        if next_page_url is not None:
            yield response.follow(next_page_url, callback=self.parse)

    def parse_product_page(self, response):
        """
        Extract info about: product, reviews
        """
        yield from self.parse_product_info(response)

    def parse_product_info(self, response):
        """
        Extract info about a product
        """
        url = response.url
        product_id = int(findall(r'(\d+)(?:\.html?$)', url)[0])
        name = response.xpath('//span[@class="goodtitle"]/text()').get()

        price_line = response.xpath('//div[@class="goodprice-line-start"]/span/span')
        if price_line:
            discount = price_line[3].xpath('text()').get()
            # if there's NO sale the first price is original
            if not discount:
                discount = 0
                discounted_price = 0
                original_price = price_line[0].xpath('text()').get()
            else:
                discount = int(discount)
                discounted_price = price_line[0].xpath('text()').get()
                original_price = price_line[2].xpath('text()').get()

        total_reviews = response.xpath('//strong[@id="js_reviewCountText"]/text()').get(default=0)
        product_info = "".join(
            txt.replace("             ", ";").strip()
            for txt in response.css('div[class="xxkkk20"] *::text').getall()
        )
        yield {
            "product_id": product_id,
            "product_url": url,
            "name": name,
            "discount": discount,
            "discounted_price": discounted_price,
            "original_price": original_price,
            "total_reviews": total_reviews,
            "product_info": product_info,
        }

    def parse_review(self, response):
        pass

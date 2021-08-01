import scrapy
from scrapy_splash import SplashRequest
from re import findall
from datetime import datetime



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
            yield SplashRequest(link, self.parse_product_page, args={'wait': 1.5})

        next_page_url = response.urljoin(response.xpath(next_page).get())
        if next_page_url is not None:
            yield response.follow(next_page_url, callback=self.parse)

    @staticmethod
    def get_product_id(url: str) -> int:
        """
        Retrieve product id from url
        """
        match = findall(r'(\d+)(?:\.html?$)', url)
        return int(match[0])

    def parse_product_page(self, response):
        """
        Extract info about: product, reviews
        """
        yield from self.parse_product_info(response)
        yield from self.parse_reviews(response)

    def parse_product_info(self, response):
        """
        Extract info about a product
        """
        product_id = self.get_product_id(response.url)
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
            "product_url": response.url,
            "name": name,
            "discount": discount,
            "discounted_price": discounted_price,
            "original_price": original_price,
            "total_reviews": total_reviews,
            "product_info": product_info,
        }

    def parse_reviews(self, response):
        """
        Extract details about reviews
        """
        if not response.xpath('//div[contains(@class, "conlist")]').get():
            return
        product_id = self.get_product_id(response.url)

        # in normal case that must retrieve page numbers, but now js is not loading ¯\_(ツ)_/¯
        # so consider following commented line variable a placeholder
        # page_numbers = response.xpath('//div[@id="js_reviewPager"]/ul/li/a/text()[.!=">"]').getall()

        page_reviews = response.xpath('//div[@class="reviewinfo table"]')
        for review in page_reviews:
            rating = len(review.xpath('.//i[@class="icon-star-black"]').getall())
            review_datetime = review.xpath('.//span[@class="review-time"]/text()').get()
            timestamp = datetime.strptime(review_datetime, "%b,%d %Y %H:%M:%S").timestamp()
            text = review.xpath('.//div[@class="review-content-text"]/text()').get()
            size = review.xpath('substring(.//span[@class="review-good-size"][1]/text(),7)').get()
            color = review.xpath('substring(.//span[@class="review-good-size"][2]/text(),8)').get()
            yield {
                "product_id": product_id,
                "rating": rating,
                "timestamp": timestamp,
                "text": text,
                "size": size,
                "color": color,
            }
        """
        Button '>' made just for a handling an event which sends GET request to get another page
        
        In my case it even didn't load
        
        In browser you can catch such GET request
        https://www.dresslily.com/m-review-a-view_review_list-goods_id-4757543-page-2?odr=0
        
        Tried to
        yield SplashRequest(f"https://www.dresslily.com/m-review-a-view_review_list-goods_id-{product_id}-page-{i}?odr=0",
                            self.parse_reviews, args={'wait': 1.5})
        ... after can't do anything with response
        End at least at one page
        """
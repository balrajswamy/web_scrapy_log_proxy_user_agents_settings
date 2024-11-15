import scrapy
from ..items import AmazonWebScrapyItem
import logging


logger = logging.getLogger(__name__)

class AmazonSpider(scrapy.Spider):

    name = "amazon"
    allowed_domains = ["www.amazon.in"]
    page_number = 1
    start_urls = ["https://www.amazon.in/s?k=Books&page=1"]
    # Set a custom User-Agent to mimic a browser
    """
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36'
    }
    """
    def parse(self, response):
        logger.info("Started parsing the response for %s", response.url)
        print(f"Current User-Agent: {response.request.headers['User-Agent']}")
        items = AmazonWebScrapyItem()

        book_titles = response.xpath('//span[@class="a-size-medium a-color-base a-text-normal"]')
        for title in book_titles:
            items["book_title"] = title.xpath('text()').get()
            #items["book_author"] = title.xpath('.//h2/a/span/text()').get()

            yield items

        # Check for the "Next" page button and follow it
        next_page = response.xpath('//a[contains(@class, "s-pagination-next")]/@href').get()
        print("next page==>", next_page)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from lantmannen.items import Article


class LantmannenSpider(scrapy.Spider):
    name = 'lantmannen'
    start_urls = ['https://www.lantmannen.se/om-lantmannen/press-och-nyheter/nyheter/']

    def parse(self, response):
        links = response.xpath('//div[@class="list-inner-wrapper--static-area"]//div[@class="callout-wrap"]/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get() or response.xpath('//h2[@class="banner-title"]/text()').get()
        if title:
            title = title.strip()

        content = response.xpath('//div[@class="content "]/div[@class="content-body"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()

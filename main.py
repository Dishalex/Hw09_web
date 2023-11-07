import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import Item, Field


class QuoteItem(Item):
    keywords = Field()
    author = Field()
    quote = Field()

class AuthorItem(Item):
    fullname = Field()
    date_born = Field()
    location_born = Field()
    bio = Field()


class QuotesSpider(scrapy.Spider):
    name = 'authors'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "result.json"}

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            keywords = quote.xpath("div[@class='tags']/a/text()").extract()
            author = quote.xpath("span/small/text()").get().strip()
            q = quote.xpath("span[@class='text']/text()").get()
            yield QuoteItem(keywords=keywords, author=author, quote=q)
            yield response.follow(url=self.start_urls[0] + quote.xpath('span/a/@href').get() , callback=self.nested_parse_author)



        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)
    
    def nested_parse_author(self, response, *args):
        author = response.xpath("html//div[@class='author-details']")
        fullname = author.xpath("h3[@class='author-title']/text()").get().strip()
        date_born = author.xpath("p/span[@class='author-born-date']/text()").get().strip()
        location_born = author.xpath("p/span[@class='author-born-location']/text()").get().strip()
        bio = author.xpath("div[@class='author-description']/text()").get().strip()
        yield AuthorItem(fullname=fullname, date_born=date_born, location_born=location_born, bio=bio)




if __name__ == '__main__':
        
    # run spider
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()
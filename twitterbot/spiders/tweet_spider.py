import scrapy


class TweetSpider(scrapy.Spider):
    name = 'tweets'

    def start_requests(self):
        urls = [
            'https://twitter.com/search?q=infosec'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.body
        print(page)

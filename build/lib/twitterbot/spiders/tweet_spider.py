import scrapy
import json
import logging
import re


class TweetSpider(scrapy.Spider):
    name = 'tweets'
    allowed_domains = ['api.scraperapi.com']

    # my custom settings
    """
    custom_settings = {
        'CONCURRENT_REQUESTS': 10, 'DOWNLOAD_DELAY': 0, 'LOG_LEVEL': 'INFO'
    }
    """

    def start_requests(self):
        urls = [
            'https://www.twitter.com/search?q=infosec',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.find_tweet)

    def find_tweet(self, response):
        tweets = response.xpath('//table[@class="tweet "]/@href').getall()
        logging.info(f'found {len(tweets)}')
        for tweet_id in tweets:
            tweet_id = re.findall("\d+", tweet_id)[-1]
            tweet_url = 'https://www.twitter.com/anuyse/status/'+str(tweet_id)
            yield scrapy.Request(tweet_url, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        print(data)

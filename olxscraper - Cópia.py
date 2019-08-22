from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class OlxSpider(CrawlSpider):
    name = "olxscraper"
    allowed_domains = ["am.olx.com.br"]
    start_urls = [
        'https://am.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios'
    ]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('.pageNextPrev',)),
             callback="parse_item",
             follow=True),)

    def parse_item(self, response):
        print('Processing..' + response.url)
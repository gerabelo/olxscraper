# -*- coding: utf-8 -*-

# Geraldo Rabelo, 30 de Julho de 2018
# geraldo.rabelo@gmail.com

import scrapy
import json

# from scrapy.utils.response import open_in_browser
from datetime import date
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver

client = MongoClient("mongodb://localhost:27017")
db = client['olx']
collection = db['carros']

class CarrosvendidosSpider(scrapy.Spider):
    name = 'carrosvendidos'
    allowed_domains = ['am.olx.com.br']
    start_urls = [
        # 'https://am.olx.com.br/regiao-de-manaus/autos-e-pecas/carros-vans-e-utilitarios/veiculo-641598366'
        'https://am.olx.com.br'
        ]

    def parse(self, response):
        docs = collection.find({
                "visible":{"$eq":True}},{'_id': False}
                # "model":{"$eq":""}},{'_id': False}
                # "url" : "https://am.olx.com.br/regiao-de-manaus/autos-e-pecas/carros-vans-e-utilitarios/troco-em-moto-de-preferencia-broz-643800337"},{'_id': False}
        )
        # ).limit(2)
        # print(response.body)
        # open_in_browser(response)
        for doc in docs:
            x = json.dumps(doc)
            y = json.loads(x)
            for key, value in y.items():
                if key == 'url':
                    print("value: "+value)
                    yield scrapy.Request(
                        response.urljoin(value),
                        callback=self.parse)

        # if response.xpath('//div[@id="ad_not_found"]/text()').get() is not None:
        x = response.css('.module_pagination a::attr(href)').extract()
        # print("x: ",x)
        if x != []:
            # print("response: ", response.request.url)
            collection.find_and_modify(query={'url':response.request.meta.get('redirect_urls')[0]}, update={"$set": {'visible': False}}, upsert=False, full_response= True)
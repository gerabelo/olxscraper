# -*- coding: utf-8 -*-

# Geraldo Rabelo, 23 de Julho de 2018
# geraldo.rabelo@gmail.com

# scrapy crawl moda.py

import scrapy
import json
from datetime import date
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver

client = MongoClient("mongodb://localhost:27017")
db = client['olx']
collection = db['moda']

class ModaSpider(scrapy.Spider):
    name = 'moda'
    allowed_domains = ['am.olx.com.br']
    start_urls = [
        # https://am.olx.com.br/regiao-de-manaus/autos-e-pecas
        # 'https://am.olx.com.br/regiao-de-manaus/autos-e-pecas/carros-vans-e-utilitarios/gm-chevrolet-s10-h-country-2-8-4x4-diesel-automatica-638029095'
        'https://am.olx.com.br/regiao-de-manaus/moda-e-beleza'
        ]

    # def parse(self, response):
    #     for page in xrange(1, 100):
    #         url = response.url + '/?o=%s' % page
    #         yield scrapy.Request(url, callback=self.parse_page)

    # def parse_page(self, response):
    #     print response.body

    def parse(self, response):
        location = ""
        phone = ""
        modelo = ""
        price = ""
        InsertedAt = ""
        description = ""

        for OLXad_list_link in response.css('.OLXad-list-link'):
            item = OLXad_list_link.css('a::attr(href)').extract_first()
            if item:
                yield scrapy.Request(
                    response.urljoin(item),
                    callback=self.parse)

        for module_pagination in response.css('.module_pagination'):
            for link in module_pagination.css('a::attr(href)').extract():
                if link:
                    yield scrapy.Request(
                    response.urljoin(link),
                    callback=self.parse)

        for OLXad_location in response.css('.OLXad-location').extract():
            soup = BeautifulSoup(OLXad_location)
            if soup:
                location = soup.get_text().replace("\t","").replace("\n","").replace("LocalizaçãoMunicípio:","").replace("CEP","").replace("Bairro","").replace(":"," ")
        
        visible_phone = response.css('.visible_phone').extract_first()
        if visible_phone:
            phone = BeautifulSoup(visible_phone).get_text().replace("\n","").replace("\t","")
        
        OLXad_date = response.css('.OLXad-date p::text')
        if OLXad_date:
            InsertedAt = OLXad_date.extract_first().replace("Inserido em: ","").replace("\n","").replace("\t","")
        
        item_model = response.css('.item.model a::text')
        if item_model:
            modelo = item_model.extract_first().replace("\n","").replace("\t","")
                    
        OLXad_id = response.css('.OLXad-id strong::text')
        if OLXad_id:
            id_ = OLXad_id.extract_first().replace("\n","").replace("\t","")
        
        OLXad_description = response.css('.OLXad-description p::text')
        if OLXad_description:
            description = OLXad_description.extract_first().replace("\n","").replace("\t","")
         
        OLXad_price = response.css('.OLXad-price span::text').extract_first()
        if OLXad_price:
            price = OLXad_price.replace("\n","").replace("\t","")

        script = BeautifulSoup(response.xpath('//script[2]').extract_first())
        if script:
            data = []
            data = json.loads(script.get_text())
            if data["name"]:
                name = data["name"]

        today = date.today()        
        # print(id_)
        # print(contato)
        # print(InsertedAt)
        # print(price)
        # print(modelo)
        
        x = collection.insert_one({"url":response.request.url,"phone":phone,"location":location,"name":name,"insertedAt":InsertedAt,"collectedIn":today.strftime("%d/%m/%Y"),"model":modelo,"price":price,"description":description,"Olx-id":id_})
        # if x.acknowledged:

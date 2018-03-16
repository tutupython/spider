# -*- coding: utf-8 -*-
import scrapy


class JycinemaSpider(scrapy.Spider):
    name = 'jycinema'
    allowed_domains = ['jycinema.com']
    start_urls = ['http://jycinema.com/']

    def parse(self, response):
        pass

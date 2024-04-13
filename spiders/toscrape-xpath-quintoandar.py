# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy import crawler


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'toscrape-xpath'
    start_urls = [
        # 'https://www.quintoandar.com.br/alugar/imovel/niteroi-rj-brasil/de-500-a-3000-reais/2-3-4-quartos/1-2-3-vagas',
        'https://www.quintoandar.com.br/alugar/imovel/icarai-niteroi-rj-brasil/de-500-a-3000-reais/2-3-4-quartos/1-2-3-vagas',
        'https://www.quintoandar.com.br/alugar/imovel/centro-niteroi-rj-brasil/de-500-a-3000-reais/2-3-4-quartos/1-2-3-vagas',
        'https://www.quintoandar.com.br/alugar/imovel/inga-niteroi-rj-brasil/de-500-a-3000-reais/2-3-4-quartos/1-2-3-vagas',
        'https://www.quintoandar.com.br/alugar/imovel/sao-domingos-niteroi-rj-brasil/de-500-a-3000-reais/2-3-4-quartos/1-2-3-vagas',
        'https://www.quintoandar.com.br/alugar/imovel/santa-rosa-niteroi-rj-brasil/de-500-a-3000-reais/2-3-4-quartos/1-2-3-vagas',
        'https://www.quintoandar.com.br/alugar/imovel/fatima-niteroi-rj-brasil/de-500-a-3000-reais/2-3-4-quartos/1-2-3-vagas'

    ]

    # handle HTTP 404 response
    handle_httpstatus_list = [404]
 
    # set the initial page count to 1
    page_count = 1

 
    def start_requests(self):
        # set the initial page default
        first_page = 1

        # start with the initial page
        for url in self.start_urls:
            url = url.replace('PAGE_VARIABLE',str(first_page))
            yield Request(url=url, callback=self.parse)


    def parse(self, response):

        # get response status
        status = response.status
 
        # terminate the crawl when you exceed the available page numbers
        if status == 404:
            self.log(f'Ignoring 404 response for URL: {response.url}')
            return
        
        for houses in response.xpath('//*[@id="__next"]/div/div/main/section[2]'):
            yield {
                'text': quote.xpath('./span[@class="text"]/text()').extract_first(),
                'author': quote.xpath('.//small[@class="author"]/text()').extract_first(),
                'tags': quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').extract()
            }
                        
 
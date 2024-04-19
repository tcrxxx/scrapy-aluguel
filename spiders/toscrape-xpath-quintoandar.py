# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy import crawler
from settings import translate_from_dict

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
                links = houses.xpath('./div/div[2]/div/div/a/@href').extract()
                addresses = houses.xpath('./div/div[2]/div/div/a/div/div/div[3]/div/h2/text()').extract()
                numeric_datas = [i.lower().split('\u00b7 ') for i in houses.xpath('./div/div[2]/div/div/a/div/div/div[3]/div/h3/text()').extract()]
                # sizes = garages[0]
                # bedrooms = garages[1]
                # garage = garages[2]
                rentValues = houses.xpath('./div/div[2]/div/div/a/div/div/div[2]/div/div[1]/div/div/span[2]/h3/text()').extract()
                totalValues = houses.xpath('./div/div[2]/div/div/a/div/div/div[2]/div/div[1]/div/div/span[1]/h3/text()').extract()

                for i in range(len(links)):
                    yield {
                        # 'link': houses.xpath('./div/div[2]/div/div/a/@href').extract_first(),
                        'link': links[i],
                        'endereco' : addresses[i],
                        'tamanho' : translate_from_dict(numeric_datas[i][0]),
                        'quartos' : translate_from_dict(numeric_datas[i][1]),
                        'banheiros' : '',
                        'garagem' : translate_from_dict(numeric_datas[i][2]),
                        'valorAluguel' : translate_from_dict(rentValues[i]),
                        'valorTaxas' : '',
                        'valorTotal' : translate_from_dict(totalValues[i])
                    }
                        
        # next_page -> //*[@id="__next"]/div/div/main/section[2]/div/div[26]/button
        # xpath = "//a[@role='button']" 
        # xpaths = driver.find_elements_by_xpath(xpath)
        # xpaths[2].click()
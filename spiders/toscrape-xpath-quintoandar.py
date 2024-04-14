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
                
                size_bed_rest_room = houses.xpath('./div/div[2]/div/div/a/div/div/div[3]/div/h3/text()').extract()
                size_bed_rest_room = [i.lower().split('\u00b7 ') for i in size_bed_rest_room]
                print(size_bed_rest_room)

                yield {
                    # 'link': houses.xpath('./div/div[2]/div/div/a/@href').extract_first(),
                    'link': houses.xpath('./div/div[2]/div/div/a/@href').extract(),
                    'endereco' : houses.xpath('./div/div[2]/div/div/a/div/div/div[3]/div/h2/text()').extract(),
                    'tamanho' : size_bed_rest_room[1],
                    'quartos' : size_bed_rest_room[2],
                    # 'banheiros' : value_restrooms_imovel,
                    # 'garagem' : size_bed_rest_room[3],
                    'valorAluguel' : houses.xpath('./div/div[2]/div/div/a/div/div/div[2]/div/div[1]/div/div/span[2]/h3/text()').extract(),
                    # 'valorTaxas' : value_tax_imovel,
                    'valorTotal' : houses.xpath('./div/div[2]/div/div/a/div/div/div[2]/div/div[1]/div/div/span[1]/h3/text()').extract()
                }
                        
        # next_page -> //*[@id="__next"]/div/div/main/section[2]/div/div[26]/button
        # xpath = "//a[@role='button']" 
        # xpaths = driver.find_elements_by_xpath(xpath)
        # xpaths[2].click()
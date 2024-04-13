# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy import crawler


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'toscrape-xpath'
    start_urls = [
        # 'https://www.zapimoveis.com.br/aluguel/imoveis/rj+niteroi/',
        'https://www.zapimoveis.com.br/aluguel/imoveis/rj+niteroi/2-quartos/?__ab=exp-aa-test:control,webp-rlt:webp,rp-imob:control,INC-Zap:vrmax14&transacao=aluguel&onde=,Rio%20de%20Janeiro,Niter%C3%B3i,,,,,city,BR%3ERio%20de%20Janeiro%3ENULL%3ENiteroi,-22.880707,-43.101353,&pagina=PAGE_VARIABLE&quartos=2&vagas=1&precoTotalMaximo=3000',
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
        
        for x in range(100):
            value_url_imovel = response.xpath("//div[@data-position='%x']/div/a/@href" % x).extract_first()
            value_street_imovel = response.xpath("//div[@data-position='%x']/div/a/div/div[1]/div[2]/div[1]/section/p//text()" % x).extract_first()
            value_size_imovel = response.xpath("//div[@data-position='%x']/div/a/div/div[1]/div[2]/section/p[1]//text()" % x).extract_first()
            value_bedrooms_imovel = response.xpath("//div[@data-position='%x']/div/a/div/div[1]/div[2]/section/p[2]//text()" % x).extract_first()
            value_restrooms_imovel = response.xpath("//div[@data-position='%x']/div/a/div/div[1]/div[2]/section/p[3]//text()" % x).extract_first()
            value_garage_imovel = response.xpath("//div[@data-position='%x']/div/a/div/div[1]/div[2]/section/p[4]//text()" % x).extract_first()
            value_rentprice_imovel = response.xpath("//div[@data-position='%x']/div/a/div/div[1]/div[2]/div[3]/div[1]/p[1]//text()" % x).extract_first()
            value_tax_imovel = response.xpath("//div[@data-position='%x']/div/a/div/div[1]/div[2]/div[3]/div[1]/p[2]//text()" % x).extract_first()

            if value_url_imovel!=None:
                yield {
                    'link': value_url_imovel,
                    'endereco' : value_street_imovel,
                    'tamanho' : value_size_imovel,
                    'quartos' : value_bedrooms_imovel,
                    'banheiros' : value_restrooms_imovel,
                    'garagem' : value_garage_imovel,
                    'valorAluguel' : value_rentprice_imovel,
                    'valorTaxas' : value_tax_imovel
                }
            
        self.page_count += 1 
        next_page = self.start_urls[0].replace('PAGE_VARIABLE',str(self.page_count))
        if self.page_count == 5:
            crawler._signal_shutdown(9,0) #Run this if the cnxn fails.
        yield Request(url=next_page, callback=self.parse)
 
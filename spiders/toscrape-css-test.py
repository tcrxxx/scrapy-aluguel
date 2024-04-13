# -*- coding: utf-8 -*-
import scrapy


class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-css"
    start_urls = [
        'https://www.zapimoveis.com.br/aluguel/imoveis/rj+niteroi/',
    ]

    def parse(self, response):
        # for quote in response.css("//*[@id='__next']/main/section/div/form/div[2]/div[4]/div[1]/div"):
        for quote in response.css("//div[@data-position='1']"):
            yield {
                'text': quote.css("//div/a/href").extract_first(),
            }

        # next_page_url = response.css("li.next > a::attr(href)").extract_first()
        # if next_page_url is not None:
        #     yield scrapy.Request(response.urljoin(next_page_url))
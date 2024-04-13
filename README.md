scrapy runspider myscrapy.py

./.venv/bin/scrapy runspider ./spiders/toscrape-xpath-zapimoveis.py -o "scraped_data/spider-$(date +'%y-%m-%d-%H-%M').json"

./.venv/bin/scrapy runspider ./spiders/toscrape-xpath-zapimoveis.py -o "scraped_data/spider-$(date +'%y-%m-%d-%H-%M').csv" -t csv

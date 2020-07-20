import scrapy
import pandas as pd


class Spider(scrapy.Spider):
    name = 'Ticker'

    # Pass in name when calling ticker spider
    def __init__(self, name: str, ticker: str, filepath, stock, *args, **kwargs):
        super(Spider, self).__init__(*args, *kwargs)
        self.name = name.replace(' ', '+')
        self.stock = stock
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                          'Chrome/83.0.4103.116 ' \
                          'Safari/537.36 Edg/83.0.478.61 '
        self.start_urls = \
            ["https://www.marketwatch.com/tools/quotes/lookup.asp?siteID=mktw&Lookup={}&Country=all&Type=All" \
                 .format(name)]

    def parse(self, response):
        ticker = response.xpath('//*[@id="symbollookup"]/div/table/tbody/tr/td[1]/a/text()').get()
        print("ticker in ticker_spider: " + ticker)
        # TODO: make it set ticker in stock through the multiprocessing
        self.stock.set_attr('ticker', ticker)
        # return ticker

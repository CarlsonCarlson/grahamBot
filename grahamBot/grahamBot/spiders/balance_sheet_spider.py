import scrapy
import pandas as pd

class Spider(scrapy.Spider):
    name = 'balance_sheet'

    def __init__(self, name, ticker, filepath, stock, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.name = name
        self.ticker = ticker
        self.filepath = filepath
        self.stock = stock
        self.start_urls = \
            [r'https://www.macrotrends.net/stocks/charts/{}/{}/balance-sheet?freq=Q'.format(ticker, name)]

    def parse(self, response):
        # TODO: figure out what he calls conservatively financed, and don't just look off the summary
        # TODO: I need to locate [long term debt, current assets, current liabilities, equity or
        #  (total assets and total liabilities)]
import scrapy
import pandas as pd
import numpy as np
import Stock


# you have to start a scrapy project

# I need to make a spider
class EPSSpider(scrapy.Spider):
    name = 'EPS'

    # Pass in name and ticker when calling EPS spider
    def __init__(self, name, ticker, filepath, stock, *args, **kwargs):
        super(EPSSpider, self).__init__(*args, *kwargs)
        self.name = name
        self.ticker = ticker
        self.filepath = filepath
        self.stock = stock
        self.start_urls = \
            ['https://www.macrotrends.net/stocks/charts/%s/%s/eps-earnings-per-share-diluted'
             % (ticker, name)]

    def parse(self, response):
        year_list = response.xpath('//*[@id="style-1"]/div[1]/table/tbody/tr/td[1]/text()').getall()
        eps_list = response.xpath('//*[@id="style-1"]/div[1]/table/tbody/tr/td[2]/text()').getall()
        # Make pandas dataframe from two lists
        year_eps_df = pd.DataFrame(np.column_stack([year_list, eps_list]),
                                   columns=['Year', 'EPS'])

        # TODO: Clean '$'s if it needs ints to run averages
        # Below doesnt work
        # year_eps_df = year_eps_df.replace(to_replace={r'$': ''}, regex=True)
        Stock.Stock.set_attr(self.stock, 'eps_df', year_eps_df)

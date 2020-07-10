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
        # Make pandas series from two lists and convert to correct data type
        year_series = pd.Series(year_list)
        year_series = pd.to_datetime(year_series)
        eps_series = pd.Series(eps_list)
        eps_series = eps_series.replace(to_replace=r'\$', value='', regex=True).astype(float)
        # Now combine them into a dataframe
        year_eps_df = pd.DataFrame(columns=['Year', 'EPS'])
        year_eps_df['Year'] = year_series
        year_eps_df['EPS'] = eps_series
        # Make dataframe compatible with the others
        year_eps_df = year_eps_df.sort_values(by='Year').reset_index(drop=True)

        # Concatenate to main dataframe
        Stock.Stock.add_first_df_to_main(self.stock, year_eps_df)

import scrapy
import pandas as pd
import numpy as np
import os.path
import Stock


# you have to start a scrapy project

# I need to make a spider
class EPSSpider(scrapy.Spider):
    name = 'EPS'

    # Pass in name and ticker when calling EPS spider
    def __init__(self, name, ticker, filepath, stock, *args, **kwargs):
        super(EPSSpider, self).__init__(*args, *kwargs)
        self.filepath = filepath
        self.stock = stock
        self.start_urls = \
            ['https://www.macrotrends.net/stocks/charts/%s/%s/eps-earnings-per-share-diluted'
             % (ticker, name)]

    def parse(self, response):
        # source is a list
        year_list = response.xpath('//*[@id="style-1"]/div[1]/table/tbody/tr/td[1]/text()').getall()
        eps_list = response.xpath('//*[@id="style-1"]/div[1]/table/tbody/tr/td[2]/text()').getall()
        # Make pandas dataframe from two lists
        year_eps_df = pd.DataFrame(np.column_stack([year_list, eps_list]),
                                   columns=['Year', 'EPS'])
        # Write file for now
        stat = response.url.split('/')[-1]
        company_name = response.url.split('/')[-2]
        ticker = response.url.split('/')[-3]
        filename = '{}({}){}.txt'.format(ticker, company_name, stat)
        complete_filename = os.path.join(self.filepath, filename)
        with open(complete_filename, 'w') as file:
            file.write(year_eps_df.to_string())
            file.close()
        Stock.Stock.set_eps(self.stock, year_eps_df)

import scrapy
import pandas as pd
import numpy as np
import os.path
import Stock


# you have to start a scrapy project

# I need to make a spider
class DividendsSpider(scrapy.Spider):
    name = 'dividends'

    # Pass in name and ticker when calling EPS spider
    def __init__(self, name, ticker, filepath, stock, *args, **kwargs):
        super(DividendsSpider, self).__init__(*args, *kwargs)
        self.name = name
        self.ticker = ticker
        self.filepath = filepath
        self.stock = stock
        self.start_urls = \
            ['https://www.macrotrends.net/assets/php/dividend_yield.php?t=%s'
             % ticker]

    def parse(self, response):
        year_list = response.xpath('/html/body/script/text()').re(r'\d\d\d\d-')
        # dividend_payout_list has '"ttm_d":' before every entry, if somehow a stock has double digit yields
        # this wont work
        dividend_payout_list = response.xpath('/html/body/script/text()').re(r'"ttm_d":\S\S\S\S')
        # TODO: if i cant get dataframe replace to work i can do a standard python replace in list using for each loop
        # Make pandas dataframe from two lists
        year_div_payout_df = pd.DataFrame(np.column_stack([year_list, dividend_payout_list]),
                                          columns=['Year', 'Dividend Payout'])

        # clean the dataframe before setting it
        # uses dict notation to replace the key with its corresponding value
        year_div_payout_df = year_div_payout_df.replace(to_replace={'-': '', r'"ttm_d":': '$'}, regex=True)
        print(year_div_payout_df.to_string())
        Stock.Stock.set_div(self.stock, year_div_payout_df)

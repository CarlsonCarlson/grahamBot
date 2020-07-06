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
        # Make pandas dataframe from two lists
        year_div_payout_df = pd.DataFrame(np.column_stack([year_list, dividend_payout_list]),
                                          columns=['Year', 'Div.Payout'])

        # clean the dataframe before setting it
        # uses dict notation to replace the key with its corresponding value
        year_div_payout_df = year_div_payout_df.replace(to_replace={'-': '', r'"ttm_d":': '$'}, regex=True)
        # TODO: if calculations are hard using quarterly, make groups by year and
        #  make new dataframe with quarterly averages as annual values
        # year_div_payout_df = year_div_payout_df.groupby(by='Year')
        # print(year_div_payout_df)

        Stock.Stock.set_attr(self.stock, "div_df", year_div_payout_df)

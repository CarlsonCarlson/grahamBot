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
        # year_list has '-' after each entry, I will need to take these out in the data frame
        year_list = response.xpath('/html/body/script/text()').re(r'\d\d\d\d-')
        # dividend_payout_list has '"ttm_d":' before every entry, if somehow a stock has double digit yields
        # this wont work
        dividend_payout_list = response.xpath('/html/body/script/text()').re(r'"ttm_d":\S\S\S\S')
        # Make pandas dataframe from two lists
        year_div_payout_df = pd.DataFrame(np.column_stack([year_list, dividend_payout_list]),
                                          columns=['Year', 'Dividend Payout'])
        # Write file for now
        # company_name = response.url.split('/')[-2]
        # ticker = response.url.split('/')[-3]
        filename = '{}({})dividend_payout.txt'.format(self.ticker, self.name)
        complete_filename = os.path.join(self.filepath, filename)
        with open(complete_filename, 'w') as file:
            file.write(year_div_payout_df.to_string())
            file.close()
        Stock.Stock.set_div(self.stock, year_div_payout_df)

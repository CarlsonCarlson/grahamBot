import scrapy
import pandas as pd
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

        # Create series of correct type
        div_series = pd.Series(dividend_payout_list)
        div_series = div_series.replace(to_replace=r'"ttm_d":', value='', regex=True)

        # if the stat series is null after cleaning we're gonna skip the rest of the code
        if div_series.isna()[0]:
            div_series = div_series.astype(float)
            year_series = pd.Series(year_list)
            year_series = year_series.replace(to_replace='-', value='', regex=True)
            year_series = pd.to_datetime(year_series)

            # Make pandas dataframe from two series
            year_div_payout_df = pd.DataFrame(columns=['Year', 'Div.Payout'])
            year_div_payout_df['Year'] = year_series
            year_div_payout_df['Div.Payout'] = div_series
            # print(year_div_payout_df)

            # clean the dataframe before setting it
            year_div_payout_df = year_div_payout_df.groupby(['Year']).mean()
            year_div_payout_df['Div.Payout'] = year_div_payout_df['Div.Payout'].round(decimals=2)
            year_div_payout_df = year_div_payout_df.set_index('Year')
            print(year_div_payout_df)
            # apparently its already a dataframe?!?!

            self.stock.concatenate_df(self.stock, year_div_payout_df)


import scrapy
import pandas as pd


# you have to start a scrapy project

# I need to make a spider
class Spider(scrapy.Spider):
    name = 'dividends'

    # Pass in name and ticker when calling EPS spider
    def __init__(self, name, ticker, filepath, stock, *args, **kwargs):
        super(Spider, self).__init__(*args, *kwargs)
        self.name = name
        self.ticker = ticker
        self.filepath = filepath
        self.stock = stock
        self.start_urls = \
            ['https://www.macrotrends.net/assets/php/dividend_yield.php?t=%s'
             % ticker]

    def parse(self, response):
        print("running dividends")
        # print("testing if i can access values in stock: ")
        # attrs = vars(self.stock)
        # print(', '.join("%s: %s" % item for item in attrs.items()))
        year_list = response.xpath('/html/body/script/text()').re(r'\d\d\d\d-')
        # dividend_payout_list has '"ttm_d":' before every entry, if somehow a stock has double digit yields
        # this wont work
        dividend_payout_list = response.xpath('/html/body/script/text()').re(r'"ttm_d":\S\S\S\S')

        # Create series of correct type
        div_series = pd.Series(dividend_payout_list)
        div_series = div_series.replace(to_replace=r'"ttm_d":', value='', regex=True)

        # Filter series for 'null' and clean data
        div_series.where(div_series != 'null', inplace=True) # Filter Series
        div_series = div_series.astype(float)
        year_series = pd.Series(year_list)
        year_series = year_series.replace(to_replace='-', value='', regex=True)
        year_series = pd.to_datetime(year_series)

        # Make pandas dataframe from two series
        year_div_payout_df = pd.DataFrame(columns=['Year', 'Div.Payout'])
        year_div_payout_df['Year'] = year_series
        year_div_payout_df['Div.Payout'] = div_series

        # clean the dataframe before setting it
        year_div_payout_df = year_div_payout_df.groupby(['Year']).mean()
        year_div_payout_df['Div.Payout'] = year_div_payout_df['Div.Payout'].round(decimals=2)
        # year_div_payout_df = year_div_payout_df.sort_values(by='Year', ascending=False)
        year_div_payout_df = year_div_payout_df.reset_index()
        # year_div_payout_df.set_index('Year', inplace=True)
        # print(year_div_payout_df)

        self.stock.concatenate_df(year_div_payout_df)

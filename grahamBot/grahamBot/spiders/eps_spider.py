import scrapy
import pandas as pd


class Spider(scrapy.Spider):
    name = 'EPS'

    # Pass in name and ticker when calling EPS spider
    def __init__(self, name, ticker, filepath, stock, *args, **kwargs):
        super(Spider, self).__init__(*args, *kwargs)
        self.name = name
        self.ticker = ticker
        self.filepath = filepath
        self.stock = stock
        self.start_urls = \
            ['https://www.macrotrends.net/stocks/charts/%s/%s/eps-earnings-per-share-diluted'
             % (ticker, name)]

    def parse(self, response):
        # print("running eps")
        # print("testing if i can access values in stock: ")
        # attrs = vars(self.stock)
        # print(', '.join("%s: %s" % item for item in attrs.items()))
        year_list = response.xpath('//*[@id="style-1"]/div[1]/table/tbody/tr/td[1]/text()').getall()
        eps_list = response.xpath('//*[@id="style-1"]/div[1]/table/tbody/tr/td[2]/text()').getall()
        # Make pandas series from two lists and convert to correct data type
        year_series = pd.Series(year_list)
        year_series = pd.to_datetime(year_series)
        eps_series = pd.Series(eps_list)
        eps_series = eps_series.replace(to_replace=r'\$', value='', regex=True)
        eps_series = eps_series.replace(to_replace=r',', value='', regex=True).astype(float)
        # Now combine them into a dataframe
        year_eps_df = pd.DataFrame(columns=['Year', 'EPS'])
        year_eps_df['Year'] = year_series
        year_eps_df['EPS'] = eps_series
        # Make dataframe compatible with the others
        year_eps_df = year_eps_df.sort_values(by='Year').reset_index(drop=True)
        # print(year_eps_df.columns)
        # year_eps_df.set_index('Year', inplace=True)
        # print(year_eps_df)

        # Concatenate to main dataframe
        self.stock.concatenate_df(year_eps_df)

        parsed_name = 'default_parsed_name'

        # set stock.name to the correct macro trends name
        if self.start_urls[0] != response.request.url:
            parsed_name = response.request.url.split('/')[-2]
            self.stock.set_attr("name", parsed_name)

        # set stock.stats['Trailing 12 Month EPS]
        quarterly_eps_list = response.xpath('//*[@id="style-1"]/div[2]/table/tbody/tr/td[2]/text()').getall()
        for eps in quarterly_eps_list[0:4]:
            eps = float(eps.strip('$'))
            self.stock.stats_dict['Trailing 12 Month EPS'] += eps

        self.stock.stats_dict['Trailing 12 Month EPS'] = \
            round(self.stock.stats_dict['Trailing 12 Month EPS'], 2)

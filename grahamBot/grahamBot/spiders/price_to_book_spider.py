import scrapy


class Spider(scrapy.Spider):
    name = 'price_to_book'

    # Pass in name and ticker when calling EPS spider
    def __init__(self, name, ticker, filepath, stock, *args, **kwargs):
        super(Spider, self).__init__(*args, *kwargs)
        self.name = name
        self.ticker = ticker
        self.filepath = filepath
        self.stock = stock
        self.start_urls = \
            ['https://www.macrotrends.net/stocks/charts/%s/%s/price-book'
             % (ticker, name)]

    def parse(self, response):
        curr_price = response.xpath('//*[@id="style-1"]/table/tbody/tr[1]/td[2]/text()').get()
        book_value_per_share = response.xpath('//*[@id="style-1"]/table/tbody/tr[2]/td[3]/text()').get()

        # Clean the data off
        curr_price = float(curr_price)
        book_value_per_share = float(book_value_per_share.strip('$'))

        # Save data
        self.stock.stats_dict['Current Price'] = curr_price
        self.stock.stats_dict['Book Value per Share'] = book_value_per_share

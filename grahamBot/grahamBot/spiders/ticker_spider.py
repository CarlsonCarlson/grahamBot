import scrapy


class Spider(scrapy.Spider):
    name = 'Ticker'

    # Pass in name when calling ticker spider
    def __init__(self, name: str, ticker: str, filepath, stock, *args, **kwargs):
        # print('Ticker spider initializing')
        super(Spider, self).__init__(*args, *kwargs)
        self.name = name.replace(' ', '+').replace('&', '%26')
        self.stock = stock
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                          'Chrome/83.0.4103.116 ' \
                          'Safari/537.36 Edg/83.0.478.61 '
        self.start_urls = \
            ["https://www.marketwatch.com/tools/quotes/lookup.asp?siteID=mktw&Lookup={}&Country=us&Type=All" \
                 .format(self.name)]

    def parse(self, response):
        # print('ticker spider parsing')
        ticker = response.xpath('//*[@id="symbollookup"]/div/table/tbody/tr/td[1]/a/text()').get()
        self.stock.set_attr('ticker', ticker)

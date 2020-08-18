import scrapy


class Spider(scrapy.Spider):
    name = 'balance_sheet'

    def __init__(self, name, ticker, filepath, stock, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.name = name
        self.ticker = ticker
        self.filepath = filepath
        self.stock = stock
        self.start_urls = \
            [r'https://www.macrotrends.net/stocks/charts/{}/{}/balance-sheet?freq=Q'.format(ticker, name)]

    def parse(self, response):
        # TODO: use correct name in url
        import datetime

        current_year = datetime.date.today().year

        # get latest date in 2020 (the current year), if blank, look in current year-1
        latest_date = response.xpath('/html/body/script').re(r'%s-[\W\d]{,5}' % current_year)[0]
        converted_latest_date = datetime.datetime.strptime(latest_date, '%Y-%m-%d').date()

        # current_date = datetime.date.today()
        #
        # quarters = [datetime.date(current_date.year, 3, 31),
        #             datetime.date(current_date.year, 6, 30),
        #             datetime.date(current_date.year, 9, 30),
        #             datetime.date(current_date.year, 12, 31)]
        # current_quarter = quarters[0]
        # for quarter in quarters:
        #     if current_date > quarter:
        #         current_quarter = quarter

        # if the latest quarter is the 4th quarter
        # if current_date < current_quarter:
        #     current_quarter = datetime.date(current_date.year - 1, 12, 31)

        # # Get quarterly data from script using:
        raw_list = response.xpath('/html/body/script').re(r'>[-,\s\w()]+<\\|"{}":"[-\w]+'.format(converted_latest_date))
        # raw_list = response.xpath('/html/body/script').re(r'>[-,\s\w()]+<\\|"{}":"[-\w]+'.format(current_quarter))

        balance_sheet_dict = {}
        category = ''
        number = ''
        for item in raw_list:
            if '>' in item:
                # it is a category
                category = item
            elif ':' in item:
                # it is a number
                number = item

            # modify and append to dict and reset to empty strings
            if category != '' and number != '':
                category = category.replace('>', '')
                category = category.replace(r"<", '')
                category = category.strip(r'\\')
                number = number.replace('"', '')
                # number = number.replace(str(current_quarter), '')
                number = number.replace(str(converted_latest_date), '')
                number = number.strip(':')
                # Turn into number into int and append to dict
                balance_sheet_dict.update({category: int(number)})
                # reset
                category = ''
                number = ''

        self.stock.set_attr('balance_sheet_dict', balance_sheet_dict)

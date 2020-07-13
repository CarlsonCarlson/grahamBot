import os
import pandas as pd
from multiprocessing import Process, Queue
import grahamBot.grahamBot.spiders as spiders
import scrapy.crawler as crawler
from twisted.internet import reactor
from scrapy.utils.log import configure_logging


# def fork(q, options_dict: dict, spider_file_name: str, stock):
#     # configure_logging()
#     try:
#         runner = crawler.CrawlerRunner()
#         if hasattr(stock, 'dir'):
#             deferred = runner.crawl(options_dict[spider_file_name], name=stock.name, ticker=stock.ticker,
#                                     filepath=stock.dir, stock=stock)
#             deferred.addBoth(lambda _: reactor.stop())
#             reactor.run()
#             q.put(None)
#         else:
#             deferred = runner.crawl(options_dict[spider_file_name], name=stock.name, ticker=stock.ticker, stock=stock)
#             deferred.addBoth(lambda _: reactor.stop())
#             reactor.run()
#             # Trying to put ticker into queue without use of any scrapy type shit.
#             # q.put(None)
#             print("stock.ticker the line after reactor.run: {}".format(stock.ticker))
#             q.put(stock.ticker)
#     except Exception as e:
#         q.put(e)
#     attrs = vars(stock)
#     print(', '.join("%s: %s" % item for item in attrs.items()))


class Stock:
    def __init__(self, name, ticker='', directory=None):
        self.name = name
        self.ticker = ticker
        # if self.ticker == '':
        #     self.name_to_ticker()
        print("ticker in init after running ticker_spider: {}".format(self.ticker))
        self.dir = directory
        self.main_df = pd.DataFrame()
        self.calculations_df = pd.DataFrame()
        self.calculations_df['Criterion:'] = ['Value:', 'Passed:', 'Note(s):']
        # if self.name is not None and self.ticker is not None:
        #     self.complete = True
        # else:
        #     self.complete = False

    # def run_spider(self, spider_file_name: str):
    # print attributes
    # attrs = vars(self)
    # print(', '.join("%s: %s" % item for item in attrs.items()))
    # Options
    # ticker_spider = spiders.ticker_spider.TickerSpider(name=self.name, stock=self)
    # print("has dir: {}".format(hasattr(self, 'dir')))
    # if hasattr(self, 'dir'):
    #     eps_spider = spiders.eps_spider.EPSSpider(name=self.name, ticker=self.ticker,
    #                                               filepath=self.dir, stock=self)
    #     dividends_spider = spiders.dividends_spider.DividendsSpider(name=self.name, ticker=self.ticker,
    #                                                                 filepath=self.dir, stock=self)
    #
    #     options_dict = {
    #         "ticker_spider": ticker_spider,
    #         "eps_spider": eps_spider,
    #         "dividends_spider": dividends_spider
    #     }
    # else:
    #     options_dict = {'ticker_spider': ticker_spider}
    #
    # Assuming that spider_file_name will be one of the options

    # queue = Queue()
    # process = Process(target=fork, args=(queue, options_dict, spider_file_name, self))
    # process.start()
    # result = queue.get()
    # process.join()
    #
    # if result is Exception:
    #     raise result
    # # I want to put my ticker, eps dataframe, div dataframe in the queue so i can get it here as result
    # print("result: {}".format(result))
    #
    # def name_to_ticker(self):
    #     # self.run_spider('ticker_spider')
    #     # print("ticker in stock.py right after running ticker_spider: " + self.ticker)
    #     from scrapy.crawler import CrawlerRunner #CrawlerProcess
    #     import grahamBot.grahamBot.spiders.ticker_spider as spider
    #     from twisted.internet import reactor, defer
    #     from scrapy.utils.log import configure_logging
    #     from crochet import setup
    #     setup()
    #     # the spider itself will set self.ticker to the correct ticker
    #     # process = CrawlerProcess({})
    #     configure_logging()
    #     runner = CrawlerRunner()
    #
    #     ticker_spider = spider.TickerSpider(name=self.name, stock=self)
    #     # ticker_crawler = process.create_crawler(crawler_or_spidercls=ticker_spider)
    #
    #     @defer.inlineCallbacks
    #     def crawl():
    #         yield runner.crawl(ticker_spider, self.name, stock=self)
    #         reactor.stop()
    #
    #     crawl()
    # reactor.run()
    # process.start(stop_after_crawl=False)
    # process.crawl(ticker_spider, self.name, stock=self)

    def set_attr(self, attribute_name: str, attribute_value) -> None:
        setattr(self, attribute_name, attribute_value)

    def concatenate_df(self, df_to_concat):
        if self.main_df.empty:
            self.main_df = df_to_concat
        else:
            self.main_df = self.main_df.merge(df_to_concat, on='Year', how='outer')
            self.main_df = self.main_df.sort_values('Year', ascending=False).reset_index(drop=True)

    def write_dataframe(self, file_name) -> None:
        # can only be used once file_path and the chosen dataframes are defined in Stock
        """
        Writes dataframe to an appropriately named file
        :param file_name: the name of the report
        """
        filename = '{}({}){}.txt'.format(self.ticker, self.name, file_name)
        complete_filename = os.path.join(self.dir, filename)
        # gets the self. of df_name
        with open(complete_filename, 'w') as file:
            file.write(self.main_df.to_string(justify='center', na_rep='None', index=True))
            file.close()

    def append_calc_result(self, calc_title: str, calc_result, criteria_passed: str, notes: str) -> None:
        """
        write the result of the calculation to self.calculations dataframe
        :param calc_title: the title of the test, this will go as a column name
        :param calc_result: the numeric result of the test, this will go in the first row
        :param criteria_passed: 'Yes' or 'No', this will go in the second row
        :param notes: Where you write any notes on exceptions that occurred
        """
        list_to_append = [calc_result, criteria_passed, notes]
        self.calculations_df[calc_title] = list_to_append

    def write_calc_report(self):
        filename = os.path.join(self.dir, '{}({})graham_report.txt'.format(self.ticker, self.name))
        with open(filename, 'w') as file:
            file.write(self.calculations_df.to_string(justify='center', index=True))
            file.close()

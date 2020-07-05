# from scrapy.crawler import CrawlerProcess
# from grahamBot.grahamBot.spiders.eps_spider import EPSSpider
# from grahamBot.grahamBot.spiders.dividends_spider import DividendsSpider
# import pandas as pd
# import numpy as np


class Stock:
    def __init__(self, name=None, ticker=None, directory=None):
        self.name = name
        self.ticker = ticker
        self.dir = directory
        self.eps_df = None
        self.div_df = None
        # TODO: when name or ticker is not found change this to do an auto complete
        if self.name is not None and self.ticker is not None:
            self.complete = True
        else:
            self.complete = False

    # TODO: make a method of getting the missing name or ticker for user

    # TODO: call eps_spider and place dataframe in eps field

    def set_dir(self, directory):
        self.dir = directory

    def set_eps(self, eps_df):
        self.eps_df = eps_df

    def set_div(self, div_df):
        self.div_df = div_df

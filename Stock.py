# from scrapy.crawler import CrawlerProcess
# from grahamBot.grahamBot.spiders.eps_spider import EPSSpider
# from grahamBot.grahamBot.spiders.dividends_spider import DividendsSpider
# import pandas as pd
# import numpy as np
import os


class Stock:
    def __init__(self, name=None, ticker=None, directory=None):
        self.name = name
        self.ticker = ticker
        self.dir = directory
        self.main_df = None
        self.eps_df = None
        self.div_df = None
        # TODO: when name or ticker is not  change this to do an auto complete
        if self.name is not None and self.ticker is not None:
            self.complete = True
        else:
            self.complete = False

    def set_dir(self, directory):
        self.dir = directory

    def set_eps(self, eps_df):
        self.eps_df = eps_df

    def set_div(self, div_df):
        self.div_df = div_df

    # TODO: finish this function once you clean div_df
    # def concatenate_df(self):
    #     self.div_df

    def write_report(self, df_name: str, report_name: str) -> None:
        # can only be used once file_path and the chosen dataframes are defined in Stock
        """
        Writes dataframe to an appropriately named file
        :param df_name: the literal name of the df field
        :param report_name: the name of the report
        """
        filename = '{}({}){}.txt'.format(self.ticker, self.name, report_name)
        complete_filename = os.path.join(self.dir, filename)
        # gets the self. of df_name
        dataframe = getattr(self, df_name)
        with open(complete_filename, 'w') as file:
            file.write(dataframe.to_string())
            file.close()

import os
import pandas as pd
from crochet import setup, wait_for
from scrapy.utils.log import configure_logging


class Stock:
    def __init__(self, name, ticker='', directory=None):
        self.name = name
        self.ticker = ticker
        self.dir = directory
        self.main_df = pd.DataFrame()
        self.calculations_df = pd.DataFrame()
        self.calculations_df['Criterion'] = []
        self.calculations_df['Value'] = []
        self.calculations_df['Passed'] = []
        self.calculations_df['Note(s)'] = []
        self.balance_sheet_dict = {}
        self.stats_dict = {'Trailing 12 Month EPS': 0,
                           'Current Price': 0,
                           'Book Value per Share': 0}

        setup()
        # configure_logging()

    @wait_for(20)
    def run_spider(self, spider_key_word: str):
        from importlib import import_module
        lower_key = spider_key_word.lower()
        module_name = "grahamBot.grahamBot.spiders.{}_spider".format(lower_key)
        imported_spider_class = import_module(module_name)  # can't seem to import using this
        arg_dict = {'name': self.name,
                    'ticker': self.ticker,
                    'filepath': self.dir,
                    'stock': self}
        spider = imported_spider_class.Spider(**arg_dict)
        from scrapy.crawler import CrawlerRunner
        crawler = CrawlerRunner()
        process = crawler.crawl(spider, **arg_dict)
        return process

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
        # list_to_append = [calc_result, criteria_passed, notes]
        # self.calculations_df[calc_title] = list_to_append
        dict_to_append = {
            "Criterion": calc_title,
            "Value": calc_result,
            "Passed": criteria_passed,
            "Note(s)": notes
        }
        self.calculations_df = self.calculations_df.append(dict_to_append, ignore_index=True)
        # self.calculations_df.set_index('Criterion', inplace=True)

    def write_calc_report(self):
        filename = os.path.join(self.dir, '{}({})graham_report.txt'.format(self.ticker, self.name))
        with open(filename, 'w') as file:
            file.write(self.calculations_df.to_string(justify='center', index=True))
            file.close()

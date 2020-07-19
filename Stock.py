import os
import pandas as pd
from crochet import setup, wait_for


# TODO: figure out where to call setup()


class Stock:
    def __init__(self, name, ticker='', directory=None):
        self.name = name
        self.ticker = ticker
        print("ticker in init after running ticker_spider: {}".format(self.ticker))
        self.dir = directory
        self.main_df = pd.DataFrame()
        self.calculations_df = pd.DataFrame()
        self.calculations_df['Criterion:'] = ['Value:', 'Passed:', 'Note(s):']
        setup()

    @wait_for(10)
    def run_spider(self, spider_key_word: str):
        from importlib import import_module
        lower_key = spider_key_word.lower()
        # upper_key = spider_key_word.capitalize()
        # module_name = ".{}_spider.{}Spider".format(lower_key, upper_key)
        # module_name = ".{}_spider".format(lower_key)
        module_name = "grahamBot.grahamBot.spiders.{}_spider".format(lower_key)
        print("importing: " + module_name)
        # imported_spider_class = import_module(module_name, package="grahamBot.grahamBot.spiders")
        imported_spider_class = import_module(module_name)
        spider = imported_spider_class.Spider(name=self.name, ticker=self.ticker, filepath=self.dir, stock=self)
        from scrapy.crawler import CrawlerRunner
        crawler = CrawlerRunner()
        process = crawler.crawl(spider)

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

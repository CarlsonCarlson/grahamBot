import pandas as pd
import numpy as np
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

    def set_attr(self, attribute_name: str, attribute_value) -> None:
        setattr(self, attribute_name, attribute_value)

    def concatenate_all_df(self):
        # TODO: combine dataframes correctly
        self.main_df = self.div_df.merge(self.eps_df, how='left')
        print(self.main_df.to_string())

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

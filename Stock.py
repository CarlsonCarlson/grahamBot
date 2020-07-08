import os
import pandas as pd


class Stock:
    def __init__(self, name=None, ticker=None, directory=None):
        self.name = name
        self.ticker = ticker
        self.dir = directory
        self.main_df = pd.DataFrame()
        self.calculations_df = pd.DataFrame()
        # TODO: when name or ticker is not change this to do an auto complete
        if self.name is not None and self.ticker is not None:
            self.complete = True
        else:
            self.complete = False

    def set_attr(self, attribute_name: str, attribute_value) -> None:
        setattr(self, attribute_name, attribute_value)

    # TODO: find how to merge/join dataframes together, when they have different years
    def add_first_df_to_main(self, df_to_concat):
        self.main_df = self.main_df.append(df_to_concat)

    def concatenate_df(self, df_to_concat):
        self.main_df = self.main_df.merge(df_to_concat, how='left')  # merge used how='left'

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
            file.write(self.main_df.to_string())
            file.close()

    def append_calc_result(self, calc_title: str, calc_result, criteria_passed: str) -> None:
        """
        write the result of the calculation to self.calculations dataframe
        :param calc_title: the title of the test, this will go as a column name
        :param calc_result: the numeric result of the test, this will go in the first row
        :param criteria_passed: 'Yes' or 'No', this will go in the second row
        """
        list_to_append = [calc_result, criteria_passed]
        self.calculations_df[calc_title] = list_to_append

    def write_calc_report(self):
        filename = os.path.join(self.dir, 'graham_report.txt')
        with open(filename, 'w') as file:
            file.write(self.calculations_df.to_string())
            file.close()

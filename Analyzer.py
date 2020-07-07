import pandas as pd

# TODO: work on Analyzer
class Analyzer:
    def __init__(self, stock):
        self.stock = stock

    def earn_inc_by_33_percent_test(self):
        # Test: diluted EPS increase by 1.33 in the past 10 years using three year
        #  averages at the beginning and end
        earnings_series = self.stock.main_df['EPS']
        # TODO: use time strp to find present date
        # TODO: access the 10th year away from present in the series
        print(earnings_series)


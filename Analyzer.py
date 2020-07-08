import pandas as pd


# TODO: work on Analyzer
class Analyzer:
    def __init__(self, stock):
        self.stock = stock

    def earn_inc_by_33_percent_test(self):
        # Test: diluted EPS increase by 1.33 in the past 10 years using three year
        #  averages at the beginning and end
        earnings_series = self.stock.main_df['EPS']
        # TODO: access the 10th year away from present in the series
        # 3 year trailing average from 10 years ago
        trailing_average_10_years_ago = earnings_series[[earnings_series.size - 11, earnings_series.size - 12,
                                                        earnings_series.size - 13]].mean()
        # 3 year trailing average since present
        trailing_average_present = earnings_series[-3:].mean().round(decimals=2)
        percent_inc = round(trailing_average_present / trailing_average_10_years_ago, 2)
        criteria_passed = 'Uncertain'
        if percent_inc >= 1.33:
            criteria_passed = 'Yes'
        elif percent_inc < 1.33:
            criteria_passed = 'No'
        self.stock.append_calc_result('EPS increased by 33%?',
                                      percent_inc, criteria_passed)

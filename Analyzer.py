import pandas as pd


# TODO: work on Analyzer
class Analyzer:
    def __init__(self, stock):
        self.stock = stock

    def earn_inc_by_33_percent_test(self):
        # Test: diluted EPS increase by 1.33 in the past 10 years using three year
        #  averages at the beginning and end
        # 3 year trailing average from 10 years ago

        current_year = pd.datetime.now().year
        df = self.stock.main_df

        # Calculate present three year trailing average
        present_3_years_filt = df['Year'].dt.year > (current_year - 3)
        present_3_years_df = df.loc[present_3_years_filt, ['Year', 'EPS']]
        most_current_year = present_3_years_df.iloc[0]['Year'].year  # We need 10 years before this year
        present_num_years_used = present_3_years_df['Year'].size
        trailing_average_present = present_3_years_df['EPS'].mean()

        # TODO: feature idea: you could make it use the most recent 3 year average from atleast 10 years ago
        #  then just report the years used in the exception.
        # Calculate 10 years ago 3 year trailing average
        past_3_year_filt = (df['Year'].dt.year <= (most_current_year - 10)) & \
                           (df['Year'].dt.year > (most_current_year - 13))
        past_3_year_df = df.loc[past_3_year_filt, ['Year', 'EPS']]
        past_num_years_used = past_3_year_df['EPS'].size
        trailing_average_past = past_3_year_df['EPS'].mean()
        if not pd.isna(trailing_average_past):  # Round it
            trailing_average_past = trailing_average_past.round(decimals=2)
        percent_inc = round(trailing_average_present / trailing_average_past, 2)

        # process calculations
        criteria_passed = 'No'  # Default
        if percent_inc >= 1.33:
            criteria_passed = 'Yes'
        elif percent_inc < 1.33:
            criteria_passed = 'No'

        # Write Note
        # expected output: 'Used 2018-2019 average and 2008-2009 average
        #  'Used 2008-2009 average
        #  'Used 2018-2019 average
        note = ''
        made_note = False
        include_and = False
        if past_num_years_used != 3:
            made_note = True
            note = note + 'Used {}-{} average'.format(past_3_year_df['Year'].min().year,
                                                      past_3_year_df['Year'].max().year)
            include_and = True
        if (present_num_years_used != 3) and include_and:
            note = note + ' and {}-{} average'.format(present_3_years_df['Year'].min().year,
                                                      present_3_years_df['Year'].max().year)
        elif present_num_years_used != 3:
            made_note = True
            note = note + 'Used {}-{} average'.format(present_3_years_df['Year'].min().year,
                                                      present_3_years_df['Year'].max().year)
        if made_note:
            note = note + ' instead of default 3 year trailing averages.'

        # Report results
        if pd.isna(percent_inc):
            self.stock.append_calc_result('EPS increased by 33%?',
                                          'No data', 'No', 'Could not find the 3 year average from {} and before.'
                                          .format(current_year - 10))
        else:
            self.stock.append_calc_result('EPS increased by 33%?',
                                          percent_inc, criteria_passed, note)

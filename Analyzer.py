import pandas as pd
import datetime


class Analyzer:
    def __init__(self, stock):
        self.stock = stock
        self.current_year = datetime.datetime.now().year

    def earn_inc_by_33_percent_test(self):
        # Test: diluted EPS increase by 1.33 in the past 10 years using three year
        #  averages at the beginning and end
        # 3 year trailing average from 10 years ago
        # TODO: fix evaluation of negative earnings per share

        # Check if there is an eps column in main_df
        if 'EPS' not in self.stock.main_df.columns:
            self.stock.append_calc_result('EPS increased by 33%?',
                                          'N/A', 'N/A', 'Could not find EPS on Macrotrends')
            return
        df = self.stock.main_df

        # Calculate present three year trailing average
        present_3_years_filt = df['Year'].dt.year > (self.current_year - 3)
        present_3_years_df = df.loc[present_3_years_filt, ['Year', 'EPS']]
        present_3_years_df.dropna(inplace=True)

        # check if empty
        if present_3_years_df.empty:
            self.stock.append_calc_result('EPS increased by 33%?',
                                          'No data', 'No', 'No EPS entries within the last 3 years')
            return
        # proceed
        most_current_year = present_3_years_df.iloc[0]['Year'].year  # We need 10 years before this year
        present_num_years_used = present_3_years_df['EPS'].size
        trailing_average_present = present_3_years_df['EPS'].mean()

        # Calculate 10 years ago 3 year trailing average
        past_3_year_filt = (df['Year'].dt.year <= (most_current_year - 10)) & \
                           (df['Year'].dt.year > (most_current_year - 13))
        past_3_year_df = df.loc[past_3_year_filt, ['Year', 'EPS']]
        past_num_years_used = past_3_year_df['EPS'].size
        trailing_average_past = past_3_year_df['EPS'].mean()
        if not pd.isna(trailing_average_past):  # Round it
            trailing_average_past = trailing_average_past.round(decimals=2)
        if trailing_average_past != 0:
            percent_inc = round(trailing_average_present / trailing_average_past, 2)
        elif trailing_average_past == 0:
            percent_inc = round(trailing_average_present / 0.01, 2)

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
        if trailing_average_past == 0:
            note = note + ' The trailing average from {}-{} was equal to 0.'.format(
                past_3_year_df['Year'].min().year, past_3_year_df['Year'].max().year)

        # Report results
        if pd.isna(percent_inc):
            self.stock.append_calc_result('EPS increased by 33%?',
                                          'No data', 'No', 'Could not find the 3 year average from {} and before.'
                                          .format(self.current_year - 10))
        else:
            self.stock.append_calc_result('EPS increased by 33%?',
                                          percent_inc, criteria_passed, note)

    def positive_earnings_test(self):
        # Check if there is an eps column in main_df
        if 'EPS' not in self.stock.main_df.columns:
            self.stock.append_calc_result('Positive earnings record?',
                                          'N/A', 'N/A', 'Could not find EPS on Macrotrends')
            return

        df = self.stock.main_df
        past_10_years_filt = df['Year'].dt.year > (self.current_year - 10)
        past_10_years_df = df.loc[past_10_years_filt, ['Year', 'EPS']]
        past_10_years_df.dropna(inplace=True)

        # check if empty
        if past_10_years_df.empty:
            self.stock.append_calc_result('Positive earnings record?',
                                          'No data', 'No', 'No EPS entries within the last 10 years')
            return
        # Proceed
        past_10_years_positive_df = past_10_years_df['EPS'] > 0

        criteria_passed = 'No'
        if past_10_years_positive_df.all():
            criteria_passed = 'Yes'

        # Report results
        self.stock.append_calc_result('Positive earnings record?',
                                      'N/A', criteria_passed, '')

    def twenty_year_div_record_test(self):
        if 'Div.Payout' not in self.stock.main_df.columns:
            self.stock.append_calc_result('Uninterrupted Div. Record?',
                                          'N/A', 'N/A', 'No Div. Payouts found on Macrotrends')
            return

        df = self.stock.main_df

        # Make 20 year div payout dataframe
        past_20_year_filt = (df['Year'].dt.year >= (self.current_year - 19))
        past_20_year_df = df.loc[past_20_year_filt, ['Year', 'Div.Payout']]
        # Filter out $0 values
        no_0_dollars_filt = (past_20_year_df['Div.Payout'] != 0)
        past_20_year_df = past_20_year_df.loc[no_0_dollars_filt, ['Year', 'Div.Payout']]
        # Filter out Nan values
        no_na_filt = (past_20_year_df['Div.Payout'].notna())
        past_20_year_df = past_20_year_df.loc[no_na_filt, ['Year', 'Div.Payout']]

        # Check if 20 values still remain
        count = len(past_20_year_df.index)
        if count < 20:
            self.stock.append_calc_result('Uninterrupted Div. Record?',
                                          count, 'No', '')
        elif count == 20:
            self.stock.append_calc_result('Uninterrupted Div. Record?',
                                          count, 'Yes', '')
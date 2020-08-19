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
                                          'N/A', 'N/A', 'Could not find EPS on MacroTrends')
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
                                          'N/A', 'N/A', 'Could not find EPS on MacroTrends')
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
                                          'N/A', 'N/A', 'No Div. Payouts found on MacroTrends')
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

    def shareholder_equity_to_total_assets(self):
        """
        total assets - total liabilities / total assets > 0.5 (Intelligent Investor 1949)
        """
        balance_sheet = self.stock.balance_sheet_dict

        # Check for Null values first
        # TODO: make the note more specific
        if 'Total Assets' not in balance_sheet or 'Total Liabilities' not in balance_sheet:
            self.stock.append_calc_result('At least 50% equity to assets ratio?', 'N/A', 'N/A', 'Not enough data found')
            return

        value = (balance_sheet['Total Assets'] - balance_sheet['Total Liabilities']) / balance_sheet['Total Assets']
        criteria_passed = ''
        if value >= 0.5:
            criteria_passed = 'Yes'
        elif value < 0.5:
            criteria_passed = 'No'

        self.stock.append_calc_result('At least 50% equity to assets ratio?', round(value, 2), criteria_passed, '')

    def long_term_debt_less_than_net_current_assets(self):
        """
        Long-term debt should be less than net working capital(current assets - current liabilities)
        """

        balance_sheet = self.stock.balance_sheet_dict

        # check for Null values first
        # TODO: make the note more specific
        if 'Long Term Debt' not in balance_sheet or 'Total Current Assets' not in balance_sheet \
                or 'Total Current Liabilities' not in balance_sheet:
            self.stock.append_calc_result('Long term debt < net current assets?', 'N/A', 'N/A', 'Not enough data found')
            return

        net_current_assets = (balance_sheet['Total Current Assets']) - (balance_sheet['Total Current Liabilities'])
        value = net_current_assets - balance_sheet['Long Term Debt']  # the surplus of net current assets to debt
        criteria_passed = ''
        if balance_sheet['Long Term Debt'] < net_current_assets:
            criteria_passed = 'Yes'
        elif balance_sheet['Long Term Debt'] >= net_current_assets:
            criteria_passed = 'No'

        self.stock.append_calc_result('Long term debt < Net Current Assets?', value, criteria_passed,
                                      'Value = Net Current Assets - Debt')

    def curr_ratio_greater_than_2(self):
        """
        Current ratio (ratio between current assets and liabilities) is greater than 2 for industrial companies
        """
        balance_sheet = self.stock.balance_sheet_dict
        if 'Total Current Assets' not in balance_sheet or 'Total Current Liabilities' not in balance_sheet:
            self.stock.append_calc_result('Current ratio > 2 ?', 'N/A', 'N/A', 'Not enough data found')
            return

        curr_ratio = balance_sheet['Total Current Assets'] / balance_sheet['Total Current Liabilities']
        criteria_passed = ''
        if curr_ratio >= 2:
            criteria_passed = 'Yes'
        elif curr_ratio < 2:
            criteria_passed = 'No, but only applicable to industrial firms'

        self.stock.append_calc_result('Current ratio > 2 ?', curr_ratio, criteria_passed, '')

    def long_term_debt_less_than_2x_shareholder_equity(self):
        """
        long term debt should not exceed 2x the share holder equity (only for public utilities)
        """
        balance_sheet = self.stock.balance_sheet_dict
        if 'Long Term Debt' not in balance_sheet or 'Share Holder Equity' not in balance_sheet:
            self.stock.append_calc_result('Long term debt < 2 * Shareholder Equity?', 'N/A', 'N/A',
                                          'Not enough data')
            return

        difference = (2 * balance_sheet['Share Holder Equity']) - balance_sheet['Long Term Debt']
        if balance_sheet['Long Term Debt'] <= (2 * balance_sheet['Share Holder Equity']):
            criteria_passed = 'Yes'
        else:
            criteria_passed = 'No, but only applicable to public utilities'

        self.stock.append_calc_result('Long term debt < 2 * Shareholder Equity?', difference, criteria_passed,
                                      'Value = Shareholder equity - Long term debt')

    def ttm_average_pe_less_than_20(self):
        """
        Trailing 12 Month Average P/E < 20 (uses eps spider to get past 4 quarters, and p/b spider for current price)
        """
        if self.stock.stats_dict['Current Price'] == 0 or self.stock.stats_dict['Trailing 12 Month EPS'] == 0:
            self.stock.append_calc_result('Trailing 12 Month Average EPS < 20 ?', 'N/A', 'N/A', 'Not enough data')
            return

        curr_price = self.stock.stats_dict['Current Price']
        ttm_average_eps = self.stock.stats_dict['Trailing 12 Month EPS']

        ttm_price_to_earnings_ratio = round(curr_price / ttm_average_eps, 2)
        if ttm_price_to_earnings_ratio <= 20:
            criteria_passed = 'Yes'
        else:
            criteria_passed = 'No'
        self.stock.append_calc_result('Trailing 12 Month Average EPS < 20 ?', ttm_price_to_earnings_ratio,
                                      criteria_passed, '')

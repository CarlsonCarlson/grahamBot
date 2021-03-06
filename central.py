import os
import pandas as pd
import pprint


def main():
    print('\t\trunning grahamBot by CarlsonCarlson @ github.com/CarlsonCarlson.....\n')
    complete = False
    while not complete:
        input_option = input('Research Single Stock(1) or Run through Fortune500 List(2)?\n Option: ')
        if input_option == '1':
            research_single()
            complete = True
        elif input_option == '2':
            run_f500()
            complete = True
        else:
            print("Option not selected. Try again")
    # research_single()
    # run_f500()
    print("Complete")


def print_stock(stock):
    # stock.main_df.set_index('Year', inplace=True)
    print(stock.main_df.to_string(justify='Center'))
    pprint.pprint(stock.balance_sheet_dict, sort_dicts=False)
    pprint.pprint(stock.stats_dict)
    # stock.calculations_df.set_index('Criterion', inplace=True)
    print(stock.calculations_df.to_string(justify='center'))


def define_filepath(ticker, name, rank: int = None, list_name: str = None) -> str:
    """
    makes directory for files to go in
    :param ticker: the ticker of the stock
    :param name: the name of the stock
    :param rank: the rank of the stock if using a list with a rank
    :param list_name: the name of the list (i.e f500, personal_watch_list
    """
    # TODO: test rank and list_name

    working_dir = os.getcwd()
    if rank is None and list_name is None:
        complete_path = os.path.join(working_dir, 'written_files')
        complete_path = os.path.join(complete_path, 'individual')
        complete_path = os.path.join(complete_path, '%s(%s)' % (ticker, name))
        print(complete_path)
    else:
        complete_path = os.path.join(working_dir, 'written_files')
        complete_path = os.path.join(complete_path, '%s' % list_name)
        complete_path = os.path.join(complete_path, '[%d]_%s(%s)' % (rank, ticker, name))
        print(complete_path)
    try:
        os.makedirs(complete_path)
    except FileExistsError:
        pass
    return complete_path


def run_all_spiders(stock):
    # Dividends goes first because it has more rows (since 1989)
    stock.run_spider('dividends')
    stock.run_spider('eps')
    stock.run_spider('balance_sheet')
    stock.run_spider('price_to_book')


def run_all_algs(stock):
    import sys
    sys.path.append("/Users/carlsoncheng/PycharmProjects/grahamBot")
    import Analyzer
    graham = Analyzer.Analyzer(stock)
    graham.earn_inc_by_33_percent_test()
    graham.positive_earnings_test()
    graham.twenty_year_div_record_test()
    graham.shareholder_equity_to_total_assets()
    graham.long_term_debt_less_than_net_current_assets()
    graham.curr_ratio_greater_than_2()
    graham.long_term_debt_less_than_2x_shareholder_equity()
    graham.ttm_average_pe_less_than_20()
    graham.price_to_seven_year_earnings_ratio_less_than_25()
    graham.price_to_3_year_earnings_less_than_15()
    graham.pb_ratio_less_than_1_point_5()
    graham.graham_number()


def research_single():
    import sys
    sys.path.append("/Users/carlsoncheng/PycharmProjects/grahamBot")
    sys.path.append("/Users/carlsoncheng/PycharmProjects/grahamBot/grahamBot/grahamBot")
    import Stock
    # TODO: make it take EITHER name or ticker, one is required though
    # name = 'apple'
    # ticker = 'AAPL'
    name = ''
    ticker = ''
    confirm = False
    while confirm is not True:
        name = input("What is the name of the stock you want to research? ")
        name = name.lower().strip()
        ticker = input("Optional: What is the ticker symbol of this stock? ")
        if ticker == '':
            sample_stock = Stock.Stock(name)  # TODO: making two stock objects
            sample_stock.run_spider('ticker')
            if sample_stock.ticker is None:
                print("No ticker found, the company may not be public")
            else:
                print("I found this ticker: " + sample_stock.ticker)
        confirm_input = input("Run? (n) to cancel and try again. \n")
        if confirm_input != 'n':
            if name != '':
                confirm = True
            else:
                print("Please enter a name. \n")
                confirm = False
        else:
            confirm = False
    if ticker == '':
        ticker = None
        stock = Stock.Stock(name)  # making two stock objects and running ticker twice
        stock.run_spider('ticker')
        complete_path = define_filepath(stock.ticker, name)
        stock.dir = complete_path
    else:
        ticker = ticker.upper()
        complete_path = define_filepath(ticker, name)
        stock = Stock.Stock(name, ticker, complete_path)
    print('Researching {}({})...'.format(stock.ticker, stock.name.capitalize()))
    run_all_spiders(stock)
    if stock.main_df.empty:
        print("I could not find any data on {}, they could be a private company".format(stock.name))
    else:
        run_all_algs(stock)
        stock.write_dataframe('main_report')
        stock.write_calc_report()
        print_stock(stock)


def run_f500():
    import sys
    sys.path.append("/Users/carlsoncheng/PycharmProjects/grahamBot")
    import Stock
    # year = input("Which f500 year do you want to run through (1955-2019)? ")
    year = '2019'
    path = 'fortune500/fortune500-' + year + '.csv'
    from time import perf_counter
    start = perf_counter()
    f500_df = pd.read_csv(path, index_col='rank', usecols=['rank', 'company'])
    count = 0
    import csv
    current_dir = os.getcwd()
    filepath = os.path.join(current_dir, 'written_files')
    filepath = os.path.join(filepath, 'errors.csv')
    with open(filepath, 'w', newline='') as error_file:
        csv_writer = csv.writer(error_file)
        csv_writer.writerow(['rank', 'company', 'error type', 'debugging notes'])
    for i in range(1, len(f500_df) + 1):
        # for i in range(325, 330):
        company = f500_df.loc[i, 'company']
        stock = Stock.Stock(f500_df.loc[i, 'company'])
        stock.run_spider('ticker')
        # Check if there is a ticker
        if stock.ticker is None:
            print("no ticker was found for " + company + " on Marketwatch lookup; proceeding to next company")
            # filepath = os.path.join(current_dir, r'written_files\errors.csv')
            current_dir = os.getcwd()
            filepath = os.path.join(current_dir, 'written_files')
            filepath = os.path.join(filepath, 'errors.csv')
            with open(filepath, 'a+', newline='') as error_file:
                csv_writer = csv.writer(error_file)
                csv_writer.writerow([i, company, 'no ticker found on Marketwatch'])

        else:
            print('Checking {}({}); Rank: {}...'.format(stock.ticker, company, i))
            run_all_spiders(stock)
            if stock.main_df.empty:
                print("I could not find any data on {} on MacroTrends, they could be a private company".
                      format(stock.name))
                current_dir = os.getcwd()
                filepath = os.path.join(current_dir, 'written_files')
                filepath = os.path.join(filepath, 'errors.csv')
                with open(filepath, 'a+', newline='') as error_file:
                    csv_writer = csv.writer(error_file)
                    csv_writer.writerow([i, company, 'stock.main_df is empty'])
            else:
                run_all_algs(stock)
                # Check if it passes the test
                filt_list = ['Yes', 'No, but only applicable to industrial firms',
                             'No, but only applicable to public utilities', 'N/A']
                passed_filt = stock.calculations_df['Passed'].isin(filt_list)
                print_stock(stock)
                if passed_filt.all():
                    count += 1
                    print_stock(stock)
    stop = perf_counter()
    print(f500_df)
    print("Time elapsed: " + str((stop - start)) + " seconds.")
    print("Time elapsed: " + str((stop - start) / 60) + " minutes.")
    print("{} stocks qualified for all tests".format(count))


if __name__ == '__main__':
    main()

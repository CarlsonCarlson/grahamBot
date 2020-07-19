import Stock
import Analyzer
import os
import pandas as pd


def main():
    print('\t\trunning grahamBot by CarlsonCarlson @ github.com/CarlsonCarlson.....\n')
    # complete = False
    # while not complete:
    #     input_option = input('Research Single Stock(1) or Run through Fortune500 List(2)?\n Option: ')
    #     if input_option == '1':
    #         research_single()
    #         complete = True
    #     elif input_option == '2':
    #         run_f500()
    #         complete = True
    #     else:
    #         print("Option not selected. Try again")
    research_single()
    print("Complete")


def define_filepath(ticker, name) -> str:
    # make directory for files to go in
    working_dir = os.getcwd()
    # print(working_dir)
    complete_path = os.path.join(working_dir, r'written_files\%s(%s)' % (ticker, name))
    # print(complete_path)
    try:
        os.makedirs(complete_path)
    except FileExistsError:
        pass
    return complete_path


def run_all_spiders(stock):
    # TODO: find out how to make spiders run in the order you want
    # Dividends goes first because it has more rows (since 1989)
    stock.run_spider('dividends')
    stock.run_spider('eps')


def run_all_algs(stock):
    graham = Analyzer.Analyzer(stock)
    graham.earn_inc_by_33_percent_test()


def research_single():
    # TODO: make it take EITHER name or ticker, one is required though
    # name = input("What is the name of the stock you want to research? ")
    # name = name.lower().strip()
    # ticker = input("What is the ticker symbol of this stock? ")
    # ticker = input("Optional: What is the ticker symbol of this stock? ")
    # if ticker == '':
    #     ticker = None
    # else:
    #     ticker = ticker.upper()
    name = 'apple'
    ticker = 'AAPL'
    # complete_path = define_filepath(ticker, name)
    # stock = Stock.Stock(name)
    # print(stock.ticker)
    # attrs = vars(stock)
    # print(', '.join("%s: %s" % item for item in attrs.items()))
    complete_path = define_filepath(ticker, name)
    stock = Stock.Stock(name, ticker, complete_path)
    print(complete_path)
    # stock.dir = complete_path
    # print(stock.dir)
    run_all_spiders(stock)
    print(stock.main_df.to_string(justify='center'))
    # stock.write_dataframe('main_report')
    # run_all_algs(stock)
    # print(stock.calculations_df.to_string(justify='center'))
    # stock.write_calc_report()


def run_f500():
    year = input("Which f500 year do you want to run through (1955-2019)? ")
    path = 'fortune500/fortune500-' + year + '.csv'
    f500_df = pd.read_csv(path, index_col='rank', usecols=['rank', 'company'])
    print(f500_df)


if __name__ == '__main__':
    main()

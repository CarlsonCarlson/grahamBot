import Stock
import os


def main():
    name = input("What is the name of the stock you want to research? ")
    name = name.lower()
    ticker = input("What is the ticker symbol of this stock? ")
    ticker = ticker.upper()
    # make directory for files to go in
    working_dir = os.getcwd()
    print(working_dir)
    complete_path = os.path.join(working_dir, r'written_files\%s(%s)' % (ticker, name))
    print(complete_path)
    try:
        os.makedirs(complete_path)
    except FileExistsError:
        pass
    stock = Stock.Stock(name, ticker, complete_path)
    stock.get_eps()
    print("Complete")


if __name__ == '__main__':
    main()

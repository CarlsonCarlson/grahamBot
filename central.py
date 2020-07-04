import Stock


def main():
    name = input("What is the name of the stock you want to research?")
    name = name.lower()
    ticker = input("What is the ticker symbol of this stock?")
    ticker = ticker.upper()
    print("Name: " + name)
    print("Ticker: " + ticker)
    stock = Stock.Stock(name, ticker)
    stock.get_eps()
    print("Complete")


if __name__ == '__main__':
    main()

from scrapy.crawler import CrawlerProcess
from grahamBot.grahamBot.spiders.dividends_spider import DividendsSpider
from grahamBot.grahamBot.spiders.eps_spider import EPSSpider
import Stock
import Analyzer
import os


def main():
    # TODO: Make it able to find the missing field (name or ticker)
    # name = input("What is the name of the stock you want to research? ")
    # name = name.lower()
    # ticker = input("What is the ticker symbol of this stock? ")
    # ticker = ticker.upper()
    name = 'walmart'
    ticker = 'WMT'
    complete_path = define_filepath(ticker, name)
    stock = Stock.Stock(name, ticker, complete_path)
    run_all_spiders(stock)
    run_all_algs(stock)
    stock.write_dataframe('main_report')
    print("Complete")


def define_filepath(ticker, name) -> str:
    # make directory for files to go in
    working_dir = os.getcwd()
    print(working_dir)
    complete_path = os.path.join(working_dir, r'written_files\%s(%s)' % (ticker, name))
    print(complete_path)
    try:
        os.makedirs(complete_path)
    except FileExistsError:
        pass
    return complete_path


def run_all_spiders(stock):
    # Dividends goes first because it has more rows (since 1989)
    process = CrawlerProcess({})
    spider1 = DividendsSpider(name=stock.name, ticker=stock.ticker, filepath=stock.dir, stock=stock)
    spider2 = EPSSpider(name=stock.name, ticker=stock.ticker, filepath=stock.dir, stock=stock)
    crawler1 = process.create_crawler(crawler_or_spidercls=spider1)
    crawler2 = process.create_crawler(crawler_or_spidercls=spider2)
    process.crawl(crawler1, stock.name, stock.ticker, stock.dir, stock=stock)
    process.crawl(crawler2, stock.name, stock.ticker, stock.dir, stock=stock)
    process.start()


def run_all_algs(stock):
    graham = Analyzer.Analyzer(stock)
    graham.earn_inc_by_33_percent_test()


if __name__ == '__main__':
    main()

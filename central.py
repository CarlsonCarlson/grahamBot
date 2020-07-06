from scrapy.crawler import CrawlerProcess
from grahamBot.grahamBot.spiders.dividends_spider import DividendsSpider
from grahamBot.grahamBot.spiders.eps_spider import EPSSpider
import Stock
import os


def main():
    name = input("What is the name of the stock you want to research? ")
    name = name.lower()
    ticker = input("What is the ticker symbol of this stock? ")
    ticker = ticker.upper()
    complete_path = define_filepath(ticker, name)
    stock = Stock.Stock(name, ticker, complete_path)
    run_all_spiders(stock)
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
    process = CrawlerProcess({})
    spider1 = EPSSpider(name=stock.name, ticker=stock.ticker, filepath=stock.dir, stock=stock)
    spider2 = DividendsSpider(name=stock.name, ticker=stock.ticker, filepath=stock.dir, stock=stock)
    crawler1 = process.create_crawler(crawler_or_spidercls=spider1)
    crawler2 = process.create_crawler(crawler_or_spidercls=spider2)
    process.crawl(crawler1, stock.name, stock.ticker, stock.dir, stock=stock)
    process.crawl(crawler2, stock.name, stock.ticker, stock.dir, stock=stock)
    process.start()


if __name__ == '__main__':
    main()

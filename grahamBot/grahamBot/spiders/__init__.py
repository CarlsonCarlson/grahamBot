# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
# for running central
from grahamBot.grahamBot.spiders.ticker_spider import Spider
from grahamBot.grahamBot.spiders.eps_spider import Spider
from grahamBot.grahamBot.spiders.dividends_spider import Spider
from grahamBot.grahamBot.spiders.balance_sheet_spider import Spider
from grahamBot.grahamBot.spiders.price_to_book_spider import Spider

# for running scrapy shell
# from grahamBot.spiders.ticker_spider import Spider
# from grahamBot.spiders.eps_spider import Spider
# from grahamBot.spiders.dividends_spider import Spider
# from grahamBot.spiders.balance_sheet_spider import Spider
# from grahamBot.spiders.price_to_book_spider import Spider

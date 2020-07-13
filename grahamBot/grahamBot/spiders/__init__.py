# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
from grahamBot.grahamBot.spiders.ticker_spider import TickerSpider
from grahamBot.grahamBot.spiders.eps_spider import EPSSpider
from grahamBot.grahamBot.spiders.dividends_spider import DividendsSpider

__all__: scrapy.Spider = ['eps_spider', 'dividends_spider', 'ticker_spider']
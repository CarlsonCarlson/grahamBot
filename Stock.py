import scrapy
from scrapy.crawler import CrawlerProcess
from grahamBot.grahamBot.spiders import eps_spider


class Stock:
    # TODO: Optional arguments so you can construct with name or ticker
    def __init__(self, name=None, ticker=None):
        self.name = name
        self.ticker = ticker
        if self.name is not None and self.ticker is not None:
            self.complete = True
        else:
            self.complete = False

    # TODO: make a method of getting the missing name or ticker for user

    # TODO: call eps_spider and place dataframe in eps field
    def get_eps(self):
        process = CrawlerProcess
        process.crawl(eps_spider, self.name, self.ticker)
        # wants a crawlerRunner object not a spider
    # do this an another function because it needs to happen after name and ticker are specified
    # self.eps =

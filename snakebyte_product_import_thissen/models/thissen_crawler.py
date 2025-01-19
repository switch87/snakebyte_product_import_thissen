from odoo import models, api
from ..controllers.thissen_crawler import ThissenCrawler

class ThissenCrawlerModel(models.TransientModel):
    _name = 'thissen.crawler'
    _description = 'Crawler for Thissen Products'

    @api.model
    def crawl_detailed_pages(self):
        crawler = ThissenCrawler(self.env)
        crawler.crawl_detailed_pages()

    @api.model
    def crawl_overview_pages(self):
        crawler = ThissenCrawler(self.env)
        crawler.crawl_overview_pages()

from scrapy.contrib.spiders.crawl import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector.unified import Selector
from buscape.items import BuscapeItem

class BuscapeSpider(CrawlSpider):
	name = "buscape_celulares"
	allowed_domains = ["buscape.com.ar"]
	start_urls = ["http://www.buscape.com.ar/celular-smartphone.html"]
	rules = [Rule(SgmlLinkExtractor(restrict_xpaths='//div[@class="description"]/a'),
			 callback='parse_item'),]
			 # Rule(SgmlLinkExtractor(restrict_xpaths='//li[@class="next"]'), follow=True),]

	def parse_item(self, response):
		item = BuscapeItem()
		sel = Selector(response)
		title = sel.xpath('//h1[@class="name"]/text()').extract()[0]
		item["title"] = title
		item["url"] = response.url
		attributes = []
		pares = sel.xpath('//*[@class="product-details"]/ul/li')
		for par in pares:
			key = par.xpath('span[@class="name"]/text()').extract()
			value = par.xpath('span[@class="value"]/text()').extract()
			attributes.append({"key": key[0], "value" : value})
		item["attributes"] = attributes
		return item

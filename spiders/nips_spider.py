from scrapy import Request
from scrapy import Spider
from articles.items import ArticlesItem

class nipsSpider(Spider):
	name = "nips_spider"
	allowed_urls = ['https://nips.cc/']
	start_urls = ['https://papers.nips.cc']
	
	def parse(self, response):
		rows = response.xpath('//li/a/@href').extract()[1:]
		for row in rows:
			url = 'https://papers.nips.cc' + row
			yield Request(url=url,meta = {'year':url[-4:]},callback=self.parse_volume_page)
	
	def parse_volume_page(self,response):
		rows = response.xpath('//li/a/@href').extract()[1:]		
		for row in rows:
			url = 'https://papers.nips.cc' + row
			yield Request(url=url,meta={'year': response.meta['year']},callback=self.parse_article_page)
	
	def parse_article_page(self,response):
		# create object ArticlesItem
		item = ArticlesItem()
		item['Title'] = response.xpath('//h2[@class="subtitle"]/text()').extract_first()
		item['Authors'] = ','.join(response.xpath('//li[@class="author"]/a/text()').extract())
		item['Year'] = response.meta['year']
		item['Volume'] = '-'
		item['Abstract'] = response.xpath('//p[@class="abstract"]/text()').extract_first().strip()
		item['Pdf_url'] = 'https://papers.nips.cc' + response.xpath('//div[@class="main wrapper clearfix"]/a/@href').extract_first()
		item['Journal_Conference'] = "NIPS"
		
		yield item
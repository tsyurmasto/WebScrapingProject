from scrapy import Request
from scrapy import Spider
from articles.items import ArticlesItem


class jmlrSpider(Spider):
	name = "jmlr_spider"
	allowed_urls = ['http://jmlr.org/']
	start_urls = ['http://jmlr.org/papers/']

	def parse(self, response):
		# extract number of volumes from http://jmlr.org/papers/
		str_last_volume = response.xpath('//font[@class="volume"]/text()').extract_first()
		nvols = int(str_last_volume.replace('Volume ',''))
		
		# construct urls of each volume page
		volume_page_urls = list(map(lambda x: 'http://jmlr.org/papers/' +'v'+str(x)+'/',list(range(1,nvols+1))))         

		for url in volume_page_urls:
			yield Request(url=url,callback=self.parse_volume_page)
		
	def parse_volume_page(self,response):
		# determine all rows inside the volume
		rows = response.xpath('//dl')

		# extract volume
		volume = response.xpath('//h1/text()').extract_first().replace('JMLR Volume ','')
		# loop over articles in the table
		for row in rows:
			title = row.xpath('./dt/text()').extract_first().strip()
			authors = row.xpath('./dd/b/i/text()').extract_first()
			year = row.xpath('./dd/text()').extract_first()[-6:-2]
			# turns out that some links contain the entire address, some are missing jmlr.org, jmlr.org/papers/, jmlr.org/papers/v? 
			abstract_url = 'http://jmlr.org/papers/v' + volume + '/' + row.xpath('./dd/a/@href').extract_first().split('/')[-1]
			pdf_url = 'http://jmlr.org/papers/v' + volume + '/' + row.xpath('./dd/a[@target="_blank"]/@href').extract_first().split('/')[-1]		

			yield Request(url=abstract_url,meta={'title':title,'authors':authors,'year':year,'volume':volume,'pdf_url':pdf_url},
				callback=self.parse_abstract_page)

	def parse_abstract_page(self,response):
		# first check abstract using @class="abstract"
		abstract = response.xpath('//p[@class="abstract"]/text()').extract_first()
		if (abstract == None):
			# extract abstract
			abstract = response.xpath('//div[@id="content"]/text()').extract()
			# remove white spaces
			abstract = list(map(lambda x: x.strip(), abstract))
			# leave on elements with at least 10 characters
			abstract = '.'.join([item for item in abstract if len(item)>1])
		else: 
			abstract = abstract.strip()
		
		# create object ArticlesItem and initialize its attributes	
		item = ArticlesItem()
		item['Title'] = response.meta['title']
		item['Authors'] = response.meta['authors']
		item['Year'] = response.meta['year']
		item['Volume'] = response.meta['volume']
		item['Pdf_url'] = response.meta['pdf_url']
		item['Abstract'] = abstract
		item['Journal_Conference'] = "JMLR"                   		
		
		yield item
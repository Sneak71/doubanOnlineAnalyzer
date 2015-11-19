# -*- coding: utf-8 -*-
import scrapy
from doubanScrapy.items import DoubanOnlineItem

class doubanOnlineSpider(scrapy.Spider):
	name = "doubanOnline"
	allowed_domains = ["douban.com"]
	#start_urls = [
	#	"http://www.douban.com/online/122763231/photo/2275011260/?sortby=time",
	#]
	def __init__(self, online1st=None):
		self.start_urls = [online1st]

	def parse(self, response):
		item = DoubanOnlineItem()
		item['link'] = response.url
		item['content'] = response.xpath('//blockquote[@class="photo-text"]/p/text()').extract()
		item['author'] = response.xpath('//div[@class="photo-ft"]/a/text()').extract()[0].encode('utf-8')
		item['date'] = response.css('div[class="photo-ft"]::text').extract()[-1].strip()[3:].encode('utf-8')
		#item['comment_author'] = ",".join(response.xpath('//div[@class="author"]/a/text()').extract()).encode("utf-8")
		#print item['date']
		item['content'] = item['content'][0].encode('utf-8').strip() if len(item['content'])>0 else ""
		yield item
		next = response.xpath('//a[@name="next_photo"]/@href').extract()[0]
		total = response.xpath('//span[@class="ll"]/text()').extract()[0]
		cur, total = total.split("/")
		#print "raw info: %s, %s" % (cur, total)
		print "total: %s, current: %s" % (total[1:-1],cur[1:-1])
		if cur[1:-1] == total[1:-1]:
			raise CloseSpider('------------------ End Search! ------------------')
		yield scrapy.Request(next, callback=self.parse)
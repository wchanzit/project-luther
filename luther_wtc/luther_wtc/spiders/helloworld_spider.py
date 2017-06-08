# -*- coding: utf-8 -*-
import scrapy

items = {'not_a_genre_at_all' : 'testing'}

class HelloWorldSpider(scrapy.Spider):
    name = "hello_world"
    allowed_domains = ["boxofficemojo.com"]
    
    
    def start_requests(self):
        start_urls = ['http://www.boxofficemojo.com/genres/']    
        
        for url in start_urls:
            #print(url)
            yield scrapy.Request(url = url, callback = self.parse)
        
    def parse(self, response):
        i = 0
        for result in response.xpath('//b/a'):
            i += 1
            if i <= 5:
                print(result)
#                print(result.xpath('./text()')) # Why does this have []?
#                print(result.xpath('./@href'))
#                print(result.xpath('./text()').extract())
#                print(result.xpath('./@href').extract())
#                print(result.xpath('./text()').extract()[0])
#                print(result.xpath('./@href').extract()[0])
#                print(result.xpath('./text()').extract_first())
#                print(result.xpath('./@href').extract_first())
            try:
                genre = result.xpath('./text()').extract()[0]
                link = result.xpath('./@href').extract()[0]
                items[genre] = response.urljoin(link)
            except:
                continue
        
        return items

# -*- coding: utf-8 -*-
import scrapy

items = {}

class MetaCriticTest1Spider(scrapy.Spider):
    name = "metacritic_test01"
    allowed_domains = ["metacritic.com"]
    
    
    def start_requests(self):
        start_urls = ['http://www.metacritic.com/movie/the-boss-baby/user-reviews?sort-by=most-helpful&num_items=100']
        
        for url in start_urls:
            #print(url)
            yield scrapy.Request(url = url, callback = self.parse)
        
    def parse(self, response):
        # In the test page, there is one tag with class "user_reviews"
        user_review_parent = response.xpath('//div[@class = "user_reviews"]')
        user_reviews = user_review_parent.xpath('./div')
        
        i = 0
        for review in user_reviews:
            #date = review.xpath('.//span[@class = "date"]/text()').extract()[0]
            
#            i += 1
#            if i <= 5:
#                print('date: ', date)
            try:
                score = review.xpath('./div[@class = "left fl"]/div/text()').extract()[0]
                author = review.xpath('.//span[@class = "author"]/a/text()').extract()[0]
                date = review.xpath('.//span[@class = "date"]/text()[not(contains("/n"))]').extract()[0]
                items[author] = [score, date]
            except:
                continue
        
#        print('i: ', i)
        return items

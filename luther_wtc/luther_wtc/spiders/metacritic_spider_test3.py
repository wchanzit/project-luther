# -*- coding: utf-8 -*-
import scrapy

items = {}

class MetaCriticTest3Spider(scrapy.Spider):
    name = "metacritic_test03"
    allowed_domains = ["metacritic.com"]
    
    
    def start_requests(self):
        # Add the letters to this list
        
        url_base = 'http://www.metacritic.com/browse/movies/title/dvd/'
        letters = list('abcdefghijklmnopqrstuvwxyz') #could import string, but w/e
        
        start_urls = [url_base + letter for letter in letters]
        start_urls.insert(0, url_base[:-1])
        #start_urls = ['http://www.metacritic.com/movie/the-boss-baby']
        
        for i, url in enumerate(start_urls):
            
            if i < 3:
                print('in start_requests; url: ', url)
                yield scrapy.Request(url = url, callback = self.getMoviePage)
        
    
    def getMoviePage(self, response):
        # Contain to A Beautiful Mind for testing 04.14 13:30
        #a_tags = response.xpath('//div[@class = "title"]/a[contains(text(), "Beautiful")]')
        
        movie_links = response.xpath('//div[@class = "title"]/a/@href').extract()
        
        #print('in getMoviePage; a_tags: ', a_tags)
        
        for j, link in enumerate(movie_links): #a_tags.xpath('./@href').extract():
            
            if j < 5:
#                print('in getMoviePage; i: ', i)
#                print('in getMoviePage; link: ', link)
#                print('in getMoviePage; urljoin(link): ', response.urljoin(link))
                
                yield scrapy.Request(url = response.urljoin(link), callback = self.getMovieInfo)

    
    def getMovieInfo(self, response):
        # In the test page, there is one tag with class "user_reviews"

        # Anchor is good to separate the overall metascores from p/m/n.
        # Use to have condition for a tag: a[@class = "metascore_anchor"], but it was unnecessary
        #print(critic.xpath('./div[contains(@class, "score")]/a/div/text()'))
                                            
        try:
            movie = response.xpath('//h1/text()').extract_first()
            genres = response.xpath('//div[@class = "genres"]/span/span').extract()
            
            # This list may complicate feeding data into a df
            genres2 = [g.replace('<span>', '').replace('</span>', '') for g in genres]
            
            rating = response.xpath('//div[@class = "rating"]/span[2]/text()').extract_first().replace('\n', '').strip()
            runtime = response.xpath('//div[@class = "runtime"]/span[2]/text()').extract_first()
            rel_date = response.xpath('//span[@class = "release_date"]/span[2]/text()').extract_first()
            
        except:
            None

        try:            
            nav = response.xpath('//*[@id="nav_to_metascore"]')
            critic = nav.xpath('./div[contains(@class, "critic")]/div[@class = "distribution"]')
            user = nav.xpath('./div[contains(@class, "user")]/div[@class = "distribution"]')

            c_score = critic.xpath('./div[contains(@class, "score")]/a/div/text()').extract_first()
            c_chart = critic.xpath('./div[contains(@class, "chart")]') #//text()
            c_pos = c_chart.xpath('./a/div[contains(@class, "positive")]/div/div[contains(@class, "count")]/text()').extract_first()
            c_mix = c_chart.xpath('./a/div[contains(@class, "mixed")]/div/div[contains(@class, "count")]/text()').extract_first()
            c_neg = c_chart.xpath('./a/div[contains(@class, "negative")]/div/div[contains(@class, "count")]/text()').extract_first()

            u_score = user.xpath('./div[contains(@class, "score")]/a/div/text()').extract_first()
            u_chart = user.xpath('./div[contains(@class, "chart")]') #//text()
            u_pos = u_chart.xpath('./a/div[contains(@class, "positive")]/div/div[contains(@class, "count")]/text()').extract_first()
            u_mix = u_chart.xpath('./a/div[contains(@class, "mixed")]/div/div[contains(@class, "count")]/text()').extract_first()
            u_neg = u_chart.xpath('./a/div[contains(@class, "negative")]/div/div[contains(@class, "count")]/text()').extract_first()

        except:
            None
        #genres2, 
        items[movie] = [genres2, rating, runtime, rel_date, c_score, c_pos, c_mix, c_neg, u_score, u_pos, u_mix, u_neg]
        
        return items

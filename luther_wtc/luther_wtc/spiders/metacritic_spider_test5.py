# -*- coding: utf-8 -*-
import scrapy

class MetaCriticTest5Spider(scrapy.Spider):
    name = "metacritic_test05"
    allowed_domains = ["metacritic.com"]
    
    custom_settings = {
                 "DOWNLOAD_DELAY": 0.025,
                 "CONCURRENT_REQUESTS_PER_DOMAIN":4,
                 "BOT_NAME":'cyrilfiggis',
                 "ROBOTSTXT_OBEY":False}

    
    def start_requests(self):
        # Add the letters to this list
        
        url_base = 'http://www.metacritic.com/browse/movies/title/dvd/'
        letters = list('abcdefghijklmnopqrstuvwxyz') #could import string, but w/e
        
        start_urls = [url_base + letter for letter in letters]
        #start_urls.insert(0, url_base[:-1]) #because $pent was giving me trouble
        
        for url in start_urls:#[:3]:
            print('in start_requests; url: ', url)
            yield scrapy.Request(url = url, callback = self.getMoviePage)
            

    
    def getMoviePage(self, response):
        # Contain to A Beautiful Mind for testing 04.14 13:30
        #a_tags = response.xpath('//div[@class = "title"]/a[contains(text(), "Beautiful")]')
        
        movie_links = response.xpath('//div[@class = "title"]/a/@href').extract()
        
        #print('in getMoviePage; a_tags: ', a_tags)
        
        for link in movie_links:#[:5]: #a_tags.xpath('./@href').extract():
            
#            print('in getMoviePage; i: ', i)
#            print('in getMoviePage; link: ', link)
#            print('in getMoviePage; urljoin(link): ', response.urljoin(link))
                
            yield scrapy.Request(url = response.urljoin(link), callback = self.getMovieInfo)
        
        nextButton = response.xpath("//span[@class='flipper next']/a/@href").extract_first()

        if nextButton:
            yield scrapy.Request(url = response.urljoin(nextButton), callback = self.getMoviePage)

    
    def getMovieInfo(self, response):
                                            
        try:
            movie = response.xpath('//h1/text()').extract_first()
            genres = response.xpath('//div[@class = "genres"]/span/span').extract()
            
            # This list may complicate feeding data into a df
            genres2 = [g.replace('<span>', '').replace('</span>', '') for g in genres]
            
            genres3 = ', '.join(genres2)
            
            rating = response.xpath('//div[@class = "rating"]/span[2]/text()').extract_first().replace('\n', '').strip()
            runtime = response.xpath('//div[@class = "runtime"]/span[2]/text()').extract_first()
            rel_date = response.xpath('//span[@class = "release_date"]/span[2]/text()').extract_first()
            
        except:
            print('EXCEPT!', response.url)
            'EMPTY' #None still returned - is this an issue?

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
            print('EXCEPT!', response.url)
            'EMPTY' #None still returned - is this an issue?

        
        yield {'movie' : movie,
               'genres' : genres3,
               'rating' : rating,
               'runtime' : runtime,
               'rel_date' : rel_date,
               'c_score' : c_score,
               'c_pos' : c_pos,
               'c_mix' : c_mix,
               'c_neg' : c_neg,
               'u_score' : u_score,
               'u_pos' : u_pos,
               'u_mix' : u_mix,
               'u_neg' : u_neg}

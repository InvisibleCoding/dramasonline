# -*- coding: utf-8 -*-
import scrapy
from dramaonline.items import DramaonlineItem

class DramasScraperSpider(scrapy.Spider):
    name = "dramas_scraper"
    allowed_domains = ["dramaonline.pk"]
    start_urls = [
        'http://dramaonline.pk/hum-tv-latest-dramas-episodes/',
        'http://dramaonline.pk/geo-tv-latest-dramas-episodes/',
        'http://dramaonline.pk/ary-digital-latest-dramas-episodes/'
        #'http://www.dramasonline.com/category/ary-digital-dramas/bulbulay/',
    ]

    def parse(self, response):
        for show_url in zip(response.xpath('//div[@class="postext"]//a/img/@alt').extract(), response.xpath('//div[@class="postext"]//a/@href').extract()):
            yield scrapy.Request(show_url[1], callback=self.parse_show)
            #print show_url

    def parse_show(self, response):
        for name_url in zip(response.xpath('//ul[@id="category-list"]//li/h2/a/@title').extract(), response.xpath('//ul[@id="category-list"]//li/h2/a/@href').extract()):
            print name_url[0],'\t',name_url[1]

        if response.xpath('//div[@class="pagination"]') and not "page" in response.url:
            num_pages = response.xpath('//div[@class="pagination"]//a/@href')[-1].extract().split('/')[-2]
            for page in range(2, int(num_pages)+1):
                next_page_url = response.url+"page/"+str(page)+"/"
                yield scrapy.Request(next_page_url, callback=self.parse_show)

    def parse_episode(self, response):
        pass

# for i in zip(response.xpath('//div[@class="postext"]//a/img/@alt').extract(), response.xpath('//div[@class="postext"]//a/@href').extract()):
#     print i

# for i in zip(response.xpath('//ul[@id="category-list"]//li/h2/a/@title').extract(), response.xpath('//ul[@id="category-list"]//li/h2/a/@href').extract()):
#     print i

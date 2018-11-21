# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import dateparser
from geopy.geocoders import Nominatim
import sys
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

class FestisCrawlerSpider(CrawlSpider):
    name = 'festis_crawler'
    allowed_domains = ['festis.es']
    start_urls = ['https://festis.es/']

    rules = (
        # Extract links with 4 consecutives numbers but without the word "cronica"
        # and don't follow links from them (since callback means follow=False by default)
        Rule(LinkExtractor(allow=(r'.*\d\d\d\d.*'), deny=(r'.*cronica.*', r'/\d\d\d\d/')), callback='parse_item'),
        # Extract links with "/page/" and follow links from them (since no
        # callback means follow=True by default)
        Rule(LinkExtractor(allow=r'.*/page/.*')),
    )

    def parse_item(self, response):
        i = {}
        i['description'] =  response.xpath(r'//*[@class="entry-content"]').extract()[0]
        loc_and_dates =     response.xpath(r'//*[@class="entry-content"]/p[last()-2]/text()[2]').extract()[0]
        i['location'] =     re.search(r'(?<=en )(.*)(?=\.)', loc_and_dates).group(0)
        try:
            geolocator = Nominatim(user_agent ="festis_crawler")
            location = geolocator.geocode(i['location'])
            i['geolocation'] = [location.longitude, location.latitude]
        except:
            i['geolocation'] = None
        try:
            start_date_day =    re.search(r'\d+', loc_and_dates).group(0)
            start_date_month =  re.search(r'(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)', loc_and_dates).group(0)
            start_date_year =   re.search(r'\d\d\d\d', loc_and_dates).group(0)
            i['start_date'] =   dateparser.parse(start_date_day + ' de ' + start_date_month + ' de ' + start_date_year, languages = ['es'])
            end_date =          re.search(r'(\d+ de (enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre).*)(?=( en))', loc_and_dates).group(0)
            i['end_date'] =     dateparser.parse(end_date, languages = ['es'])
        except:
            i['start_date'] = None
            i['end_date'] = None
        i['category_url'] = response.xpath(r'//*[@class="entry-content"]/p[last()-2]/a[1]/@href').extract()[0]
        try:
            i['twitter'] =  response.xpath(r'//*[@class="entry-content"]/p[last()-1]/a[3]/@href').extract()[0]
        except:
            i['twitter'] = None
        try:
            i['facebook'] = response.xpath(r'//*[@class="entry-content"]/p[last()-1]/a[2]/@href').extract()[0]
        except:
            i['facebook'] = None
        i['name'] =         response.xpath(r'//*[@class="entry-content"]/p[last()-2]/strong/text()').extract()[0] + ' ' + start_date_year
        i['web'] =          response.xpath(r'//*[@class="entry-content"]/p[last()-1]/a[1]/@href').extract()[0]
        i['entry_date'] =   response.xpath(r'//*[@class="entry-header"]/div/span[2]/time[1]/@datetime').extract()[0]
        i['entry_title'] =   response.xpath(r'//*[@class="entry-header"]/h1/text()').extract()[0]
        i['entry_image'] =   response.xpath(r'(//img/@src)[2]').extract()[0]
        i['url'] =          response.url
        return i

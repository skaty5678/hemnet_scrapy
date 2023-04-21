import scrapy
from scrapy import signals
from pydispatch import dispatcher
import json
import time


# Define the Spider class
class HemnetSpider(scrapy.Spider):
    
    # Set the name of the spider
    name = "hemnet"
    
     # Set the URL to start crawling from
    start_urls = ['https://www.hemnet.se/bostader?location_ids%5B%5D=474361&item_types%5B%5D=villa']
    
    # Initialize a counter and a dictionary to store results
    counter=0
    results = {}
    
    # Define a method that will be called when the spider is initialized
    def __init__(self):
        # Connect the spider_closed method to the spider_closed signal
        dispatcher.connect(self.spider_closed, signals.spider_closed)


    # Define the method that will be used to parse the response from the start_urls
    def parse(self, response):
        
        # Iterate over the ads on the page and extract the URL of the ad
        for ad in response.css("ul.normal-results > li.normal-results__hit > a::attr('href')"):
            # Wait for 2 seconds before sending a request to avoid overloading the website
            time.sleep(2)
            # Send a request to the ad URL and parse the response using the parseinnerpage method
            yield scrapy.Request(url=ad.get(), callback=self.parseinnerpage)
        
        # Extract the URL of the next page and follow it if it exists
        nextpage = response.css("a.next_page::attr('href')").get()
        
        if nextpage is not None:
            # Wait for 1 second before following the URL to avoid overloading the website
            time.sleep(1)
            response.follow(nextpage, self.parse)

    # Define the method that will be used to parse the response from an ad URL
    def parseinnerpage(self, response):

        # Extract the street name from the response
        
        streetname = response.css("h1.qa-property-heading::text").get()
        # Extract the price from the response and clean it up
        price = response.css('p.property-info__price::text').get()
        price = price.replace('kr','')
        price = price.replace(u'\xa0','')
        print(price)

        # Extract the attributes from the response and store them in a dictionary
        attrData = {}
        for attrs in response.css("div.property-attributes > div.property-attributes-table > dl.property-attributes-table__area > div.property-attributes-table__row"):
            attrlabel = attrs.css('dt.property-attributes-table__label::text').get()
            if attrlabel is not None:
                attrlabel = attrlabel.replace(u'\n','')
                attrlabel = attrlabel.replace(u'\t','')
                attrlabel = attrlabel.replace(u'\xa0','')
                attrlabel = attrlabel.strip('')
            print(attrlabel)
            attrvalue = attrs.css('dd.property-attributes-table__value::text').get()
            if attrvalue is not None:
                attrvalue = attrvalue.replace(u'\n','')
                attrvalue = attrvalue.replace(u'\t','')
                attrvalue = attrvalue.replace('kr/mån','')
                attrvalue = attrvalue.replace('kr/år','')
                attrvalue = attrvalue.replace('kr/m²','')
                attrvalue = attrvalue.replace('m²','')
                attrvalue = attrvalue.replace(u'\xa0','')
                attrvalue = attrvalue.replace(' ', '')
                attrvalue = attrvalue.strip('')
            
            # If there is a valid attribute label, add the attribute value to the dictionary
            if attrlabel is not None:
                attrData[attrlabel] = attrvalue
        
        # Create a new entry in the results dictionary for the current property
        # with its street name, price, and attributes
        self.results[self.counter] = {
            "street name":streetname,
            'price': price,
            'attrs': attrData
        }

        # Increase the counter by 1 to keep track of the number of properties scraped
        self.counter = self.counter + 1

    # When the spider is closed, write the results dictionary to a JSON file
    def spider_closed(self, spider):
        with open('results.json','w') as f:
            json.dump(self.results, f, ensure_ascii=False)
# Hemnet Spider


## Description

The Hemnet Spider is a web crawler built using Scrapy, a Python-based web scraping framework. The spider crawls the hemnet.se website to extract information about villas for sale in a Sweden. The extracted information includes the street name, price, and various attributes such as number of rooms, living area, and plot size.


## Usage

### To use the Hemnet Spider, follow these steps:

1. Install Scrapy by running the following command in your terminal:
*pip install scrapy*.

2. Clone this repository to your local machine:
*git clone https://github.com/skaty5678/hemnet_scrapy.git*.

3. Navigate to the hemnet directory: cd hemnet.

4. Run the spider using the following command: scrapy crawl hemnet.

5. Wait for the spider to finish crawling. The scraped data will be saved to a results.json file in the hemnet-spider directory.


## Customization

To customize the spider to crawl a different location or type of property, modify the *start_urls* variable in the HemnetSpider class. For example, to crawl villas for sale in a different location, change the location_ids parameter in the URL:


*start_urls = ['https://www.hemnet.se/bostader?location_ids%5B%5D=123456&item_types%5B%5D=villa']*

To crawl a different type of property, change the item_types parameter in the URL:

*start_urls = ['https://www.hemnet.se/bostader?location_ids%5B%5D=474361&item_types%5B%5D=radhus']*







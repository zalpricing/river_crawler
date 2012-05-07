import lxml.html as LH
import urllib2
import csv
import os, errno
from lxml.cssselect import CSSSelector as CS
from lxml.etree import fromstring as FS
from datetime import date

d = date.fromordinal(730920)
day = d.strftime("%Y%m%d")

config = { 
    'amazon': { 
        'sale-price':'/html/body//table[@class="product"]//b[@class="priceLarge"]',
        'list-price':'/html/body//table[@class="product"]//td[@class="listprice"]',
#        'range-price':'/html/body//table[@class="product"]//span[@class="priceLarge"]',
#        'normal-price':'/html/body//table[@class="product"]//span[@class="priceLarge"]',
#        'title':'...',
        'brand':'//table[@class="techSpecTable"]/tr/tr[@class="techSpecTD2"]',
#        'retailer':'...',
#        'category':'...',
        'id':'//div[@class="content"]/ul/li',
    }
}

url='http://www.amazon.de/Loake-Aldwych-Klassische-Halbschuhe-schwarz/dp/B002OR8MCA/ref=twister_dp_update?ie=UTF8&psc=1'

def request_html(target_url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    opened_url = opener.open(target_url)
    html = LH.parse(opened_url)
    return html

def parse_target(raw_data, target):
    crawl_output = []
    crawl_output.append(url)
    crawl_config = config[target]
    for key, value in crawl_config.items():
        raw_crawl = raw_data.xpath(value)
        if not raw_crawl == []:
            crawl = raw_crawl[0].text
            crawl_output.append(crawl)
        else: 
            crawl_output.append('not found')
    return crawl_output

def write_csv(parsed_data, csvfile):
    with open(csvfile, 'a') as file:
        listwriter = csv.writer(file, delimiter=';')
        listwriter.writerows(parsed_data)


# OUTPUT FILE
output_file = day + '_amazon_output_python.csv'

# START SCRAPING
html_data = request_html(url)
parsed_data = [parse_target(html_data, 'amazon')]
print(parsed_data)
write_csv(parsed_data, output_file)
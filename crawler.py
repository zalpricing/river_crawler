# River Crawler 1.0 - Sebastian Oehlschläger, Torsten Kunz

import lxml.html as LH
import urllib2, csv, os, errno, time
from string import Template
from lxml.cssselect import CSSSelector as CS
from lxml.etree import fromstring as FS
from datetime import date

today = date.today()
day = today.strftime("%Y%m%d")

config = { 
    'amazon': {
        'url':'http://www.amazon.de/gp/product/$sku/ref=twister_dp_update?ie=UTF8&psc=1',
        'sale-price':'/html/body//table[@class="product"]//b[@class="priceLarge"]',
        'list-price':'/html/body//table[@class="product"]//td[@class="listprice"]',
        'range-price':'/html/body//table[@class="product"]//span[@class="priceLarge"]',
        'normal-price':'/html/body//table[@class="product"]//b[@class="priceLarge"]',
        'title':'...',
        'brand':'//table[@class="techSpecTable"]/tr/tr[@class="techSpecTD2"]',
        'retailer':'...',
        'category':'...',
        'id':'//div[@class="content"]/ul/li',
    }
}

# url='http://www.amazon.de/Loake-Aldwych-Klassische-Halbschuhe-schwarz/dp/B002OR8MCA/ref=twister_dp_update?ie=UTF8&psc=1'

def request_html(target_url):
    try:
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        opened_url = opener.open(target_url)
        html = LH.parse(opened_url)
        return html
    except:
        html = "Failed request"
        return html

def parse_target(raw_data, target):
    crawl_output = []
    crawl_config = config[target]
    for key, value in crawl_config.items():
        try:
            raw_crawl = raw_data.xpath(value)
            if not raw_crawl == []:
                crawl = raw_crawl[0].text.encode('latin-1')
                crawl_output.append(crawl)
        except Exception:
            crawl_output.append('not found')
    return crawl_output

def read_csv(csvfile):
     reader = csv.reader(open(csvfile, 'r'), delimiter=';')
     return reader
    
def write_csv(parsed_data, csvfile):
    with open(csvfile, 'a') as file:
        listwriter = csv.writer(file, delimiter=';')
        listwriter.writerows(parsed_data)

# INPUT 
input_file = 'input/amazon_input.csv'

# OUTPUT FILE
output_file = day + '_amazon_output_python.csv'

# START SCRAPING
crawl_input = read_csv(input_file)
write_csv([['starttime', time.strftime("%H:%M", time.localtime())]],output_file)
for line in crawl_input:
    target = line[2]
    raw_url = Template(config[target]['url'])
    url = str(raw_url.substitute(sku=line[1]))

    html_data = request_html(url)
    if html_data == "Failed request":
        continue

    parsed_data = parse_target(html_data, target)

    output = [line[0], url]
    output.append(parsed_data)
    print(output)
    write_csv([output], output_file)
write_csv([['endtime', time.strftime("%H:%M", time.localtime())]],output_file)
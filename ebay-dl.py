import argparse
from ctypes.wintypes import tagSIZE
from fileinput import filename
import requests
from bs4 import BeautifulSoup
import json
import csv


def parse_price(text):
    text=text.replace('$','')
    text=text.replace('.','')
    text=text.replace(',','')
    text=text.split()

    try:
        text=int(text[0])
        return text
    except:
        return text 


#finsh
def parse_shipping(text):
        if 'free' in text.lower():
            return 0
        else:
            text=text.replace('$','')
            text=text.replace('.','')
            text=text.replace('+','')
            text=text.split()
            return int(text[0])
    
def parse_itemssold(text):  
    numbers = ''
    for char in text:
        if char in '1234567890':
            numbers += char
    if 'sold' in text:
        return int(numbers)
    else:
        return 0

# get command line arguments
parser = argparse.ArgumentParser(description='download ebay information and convert to JSON')
parser.add_argument('search_term')
parser.add_argument('--num_pages', default=10)
parser.add_argument('--csv', default=False)
args = parser.parse_args()

print('args.search_terms=', args.search_term)

# list of all ebay items
items = []

# loop over ebay webpages
for page_number in range(1,int(args.num_pages)+1):
    # build the url
    url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=' + args.search_term + '&_sacat=0&_pgn=' + str(page_number)

    #download html
    r = requests.get(url)
    status = r.status_code

    html = r.text

    # process html
    soup = BeautifulSoup(html, 'html.parser')

    # loop over items in page
    tags_items = soup.select('.s-item')
    for tag_item in tags_items:

        name = None
        tags_name = tag_item.select('.s-item__title')
        for tag in tags_name:
            name = tag.text

        price = None
        tags_price = tag_item.select('.s-item__price')
        for tag in tags_price:
            price = parse_price(tag.text)

        status = None
        tags_status = tag_item.select('.SECONDARY_INFO')
        for tag in tags_status:
            status = tag.text
        
      
        shipping = None
        tags_status = tag_item.select('.s-item__shipping')
        for tag in tags_status:
            shipping = parse_shipping(tag.text)
        

        
        
        free_returns = False
        tags_free_returns = tag_item.select('.s-item__free-returns')
        for tag in tags_status:
            free_returns = tag.text


        items_sold = None
        tags_itemssold = tag_item.select('.s-item__hotness, .s-item__additionalItemhotness')
        for tag in tags_itemssold:
            items_sold = parse_itemssold(tag.text)

        item ={
            'name': name,
            'price': price,
            'status': status,
            'shipping': shipping,
            'free_returns': free_returns,
            'items_sold': items_sold
        }
        
        if 'Shop on eBay' in item['name']:
                continue
        else:
            items.append(item)

#csv file 
if bool(args.csv) == True:
    csv_columns= ['name', 'price', 'status', 'shipping', 'free_returns', 'items_sold']
    filenamecsv = args.search_term+'.csv'
    filenamecsv = filenamecsv.replace(" ", "_")
    with open(filenamecsv, 'w', newline='', encoding='utf-8') as f:
        ebaycsv = csv.DictWriter(f, fieldnames=csv_columns)
        ebaycsv.writeheader()
        for item in items:
            ebaycsv.writerow(item)

#json file 
else:
    filename = args.search_term+'.json'
    filename = filename.replace(" ", "_")
    with open(filename, 'w', encoding='utf-8') as fj:
        fj.write(json.dumps(items))
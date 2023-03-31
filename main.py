from datetime import datetime
import json
import sys
import re
sys.path.append("./src")

import cld3

from facebook.Marketplace import *
from gmail import gmail

LATITUDE = "40.4016"
LONGITUDE = "-74.3063"
NOW = datetime.now()
CATEGORIES = ["bicycle", "rug", "couch", "furniture", "free", "table", "computer", "tv", "homegoods"]

def score_listings(listings):
        
    for listing in listings: 
        listing['score'] = 0
        
        ### DISQUALIFIER ### 
        # Not English
        translation = cld3.get_language(listing['title'])
        if ((translation.language == "es" and translation.is_reliable) or any(c in listing['title'] for c in ['ñ', 'é', 'á', 'ó'])):
            listing['score'] = -50
        
        # Cheap
        price = float(listing['currentPrice'][1:].replace(',', ''))
        if (price == 0 and "$" in listing['description']):
            price_list = re.findall(r'\$(\d+)', listing['description'])
            if (len(price_list) != 0):
                price_list_int = list(map(int, price_list))
                price = sum(price_list_int) / len(price_list_int)
                listing['price'] = price
        listing['score'] += (250 - price)/25

        # Recent
        if (isinstance(listing['timestamp'], datetime)):
            timestamp = listing['timestamp']
        else:
            timestamp = datetime.strptime(listing['timestamp'], "%Y-%m-%d %H:%M:%S")
        delta = NOW - timestamp
        hours_since_post = delta.days * 24 + delta.seconds/3600
        listing['score'] += 10 - (hours_since_post/24)
        
        # Score differently for different categories
        category_dict = {
            "furniture" : 15,
            "rug" : 10,
            "couch" : 8,
            "table" : 8,
            "homegoods" : 6,
            "tv" : 5,
            "bicycle" : 5,
            "free" : -2,
            "plants" : -1
        }
        
        listing['score'] += category_dict.get(listing['category'], 0)
        
        # Good quality
        condition_dict = {
            "New" : 5,
            "Used - like new" : 3,
            "Used - fair" : -3
        }
        listing['score'] += condition_dict.get(listing['condition'], 0)
        
        # Location
        if ("New York" in listing['sellerLocation']):
            listing['score'] -= 15

    listings.sort(reverse=True, key=lambda x: x['score'])
    return listings

def populate_listings(listings, output=True):
    
    if output:
        with open("sample.json", "w") as outfile:
            outfile.write('{"listings":[')
            for listing in listings:
                test = listing
                outfile.write(json.dumps(test, indent=4, default=str))
                outfile.write(',')
            outfile.write(']}')
    
    return listings

if __name__ == "__main__":
    
    listings = []
    
    # STEP 1 - Get listings
    facebook_marketplace = Marketplace(LATITUDE, LONGITUDE)
    
    for category in CATEGORIES:
        print("Checking Facebook Marketplace listings for query: " + category)
        listings.extend(facebook_marketplace.get_listings(category))
        
    # or ...
    # import json
    # f = open('sample.json')
    # data = json.load(f)
    # for item in data['listings']:
    #     listings.append(item)
    
    #STEP 2 - Score all listings
    listings = score_listings(listings)
    listings = populate_listings(listings)
    
    # STEP 3 - Send email of top 10 listings
    gmail.send_email_old(listings[:10])
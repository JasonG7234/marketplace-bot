from datetime import datetime
import json
import sys
sys.path.append("./src")

from facebook.Marketplace import *
from gmail import gmail

LATITUDE = "40.4016"
LONGITUDE = "-74.3063"
NOW = datetime.now()
CATEGORIES = ["bicycle", "rug", "couch", "furniture", "free", "table", "computer", "tv", "homegoods"]

def score_listings(listings):
        
    for listing in listings: 
        listing['score'] = 0
        
        # Cheap
        price = int(listing['currentPrice'][1:].replace(',', ''))
        listing['score'] += (250 - price)/25

        # Recent
        if (isinstance(listing['timestamp'], datetime.datetime)):
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

    listings.sort(reverse=True, key=lambda x: x['score'])
    return listings

def populate_listings(listings, output=True):
    
        
    if output:
        with open("sample.json", "w") as outfile:
            outfile.write('{"listings":[')
            for listing in listings:
                test = listing
                test['positiveVotes'] = 0
                test['negativeVotes'] = 0
                outfile.write(json.dumps(test, indent=4, default=str))
                outfile.write(',')
            outfile.write(']}')
    
    return listings

if __name__ == "__main__":
    
    # STEP 1 - Get listings
    facebook_marketplace = Marketplace(LATITUDE, LONGITUDE)
    listings = []
    
    for category in CATEGORIES:
        listings.extend(facebook_marketplace.get_listings(category))
    
    # STEP 2 - Score all listings
    listings = score_listings(listings)
    listings = populate_listings(listings)
    
    # STEP 3 - Send email of top 10 listings
    gmail.send_email(listings[:10])
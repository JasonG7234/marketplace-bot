import sys
sys.path.append("./src")

from facebook.Marketplace import *

import json

LATITUDE = "40.4016"
LONGITUDE = "-74.3063"

facebook_marketplace = Marketplace()
listings = []

listings.extend(facebook_marketplace.get_listings(LATITUDE, LONGITUDE, "rug"))
listings.extend(facebook_marketplace.get_listings(LATITUDE, LONGITUDE, "couch"))
listings.extend(facebook_marketplace.get_listings(LATITUDE, LONGITUDE, "basketball"))
listings.extend(facebook_marketplace.get_listings(LATITUDE, LONGITUDE, "furniture"))
listings.extend(facebook_marketplace.get_listings(LATITUDE, LONGITUDE, "free"))
listings.extend(facebook_marketplace.get_listings(LATITUDE, LONGITUDE, "table"))
listings.extend(facebook_marketplace.get_listings(LATITUDE, LONGITUDE, "video games"))
listings.extend(facebook_marketplace.get_listings(LATITUDE, LONGITUDE, "computer"))
listings.extend(facebook_marketplace.get_listings(LATITUDE, LONGITUDE, "plants"))
listings.extend(facebook_marketplace.get_listings(LATITUDE, LONGITUDE, "tv"))
listings.extend(facebook_marketplace.get_listings(LATITUDE, LONGITUDE, "electronics"))
listings.extend(facebook_marketplace.get_listings(LATITUDE, LONGITUDE, "technology"))
listings.extend(facebook_marketplace.get_listings(LATITUDE, LONGITUDE, "men"))
listings.extend(facebook_marketplace.get_listings(LATITUDE, LONGITUDE, "homegoods"))


with open("sample.json", "w") as outfile:
    outfile.write('{"listings":[')
    for listing in listings:
        test = listing
        test['positiveVotes'] = 0
        test['negativeVotes'] = 0
        outfile.write(json.dumps(test, indent=4, default=str))
        outfile.write(',')
    outfile.write(']}')

    

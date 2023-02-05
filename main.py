import sys
sys.path.append("./src")

from facebook.Marketplace import *

import json

LATITUDE = "40.4016"
LONGITUDE = "-74.3063"

facebook_marketplace = Marketplace(LATITUDE, LONGITUDE)
listings = []

listings.extend(facebook_marketplace.get_listings("bicycle", debug_mode=True))
listings.extend(facebook_marketplace.get_listings("rug"))
listings.extend(facebook_marketplace.get_listings("couch"))
listings.extend(facebook_marketplace.get_listings("basketball"))
listings.extend(facebook_marketplace.get_listings("furniture"))
listings.extend(facebook_marketplace.get_listings("free"))
listings.extend(facebook_marketplace.get_listings("table"))
listings.extend(facebook_marketplace.get_listings("video games"))
listings.extend(facebook_marketplace.get_listings("computer"))
listings.extend(facebook_marketplace.get_listings("plants"))
listings.extend(facebook_marketplace.get_listings("tv"))
listings.extend(facebook_marketplace.get_listings("electronics"))
listings.extend(facebook_marketplace.get_listings("technology"))
listings.extend(facebook_marketplace.get_listings("men"))
listings.extend(facebook_marketplace.get_listings("homegoods"))

# FOR THE ALGORITHM - IN ORDER...
# Prioritze FREE over PAID, scaling for the amount of money
# Prioritize RECENT POSTINGS, scaling for the recency of the post
# Prioritize CATEGORY
    # Delete entries if they've been shown to me before
# Prioritize good condition, scaling
# Prioritize proximity

with open("sample.json", "w") as outfile:
    outfile.write('{"listings":[')
    for listing in listings:
        test = listing
        test['positiveVotes'] = 0
        test['negativeVotes'] = 0
        outfile.write(json.dumps(test, indent=4, default=str))
        outfile.write(',')
    outfile.write(']}')

    

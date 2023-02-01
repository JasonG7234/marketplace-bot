import requests
import json
import copy
import time

GRAPHQL_URL = "https://www.facebook.com/api/graphql/"
GRAPHQL_HEADERS = {
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"
}

def getLocations(locationQuery):
    data = {}

    requestPayload = {
        "variables": """{"params": {"caller": "MARKETPLACE", "page_category": ["CITY", "SUBCITY", "NEIGHBORHOOD","POSTAL_CODE"], "query": "%s"}}""" % (locationQuery),
        "doc_id": "5585904654783609"
    }

    status, error, facebookResponseJSON = getFacebookResponse(requestPayload)

    if (status == "Success"):
        data["locations"] = []  # Create a locations object within data

        # Get location names and their ID from the facebook response
        for location in facebookResponseJSON["data"]["city_street_search"]["street_results"]["edges"]:
            locationName = location["node"]["subtitle"].split(" \u00b7")[0]

            # Refine location name if it is too general
            if (locationName == "City"):
                locationName = location["node"]["single_line_address"]

            locationLatitude = location["node"]["location"]["latitude"]
            locationLongitude = location["node"]["location"]["longitude"]

            # Add the location to the list of locations
            data["locations"].append({
                "name": locationName,
                "latitude": str(locationLatitude),
                "longitude": str(locationLongitude)
            })

    return (status, error, data)


def getListings(locationLatitude, locationLongitude, listingQuery, numPageResults=1):
    data = {}

    rawPageResults = []  # Un-parsed list of JSON results from each page

    requestPayload = {
        "variables": """{"count":24, "params":{"bqf":{"callsite":"COMMERCE_MKTPLACE_WWW","query":"%s"},"browse_request_params":{"commerce_enable_local_pickup":true,"commerce_enable_shipping":true,"commerce_search_and_rp_available":true,"commerce_search_and_rp_condition":null,"commerce_search_and_rp_ctime_days":null,"filter_location_latitude":%s,"filter_location_longitude":%s,"filter_price_lower_bound":0,"filter_price_upper_bound":214748364700,"filter_radius_km":16},"custom_request_params":{"surface":"SEARCH"}}}""" % (listingQuery, locationLatitude, locationLongitude),
        "doc_id": "7111939778879383"
    }

    status, error, facebookResponse = getFacebookResponse(requestPayload)

    if (status == "Success"):
        rawPageResults.append(facebookResponse)

        # Retrieve subsequent page results if numPageResults > 1
        for _ in range(1, numPageResults):
            pageInfo = facebookResponse["data"]["marketplace_search"]["feed_units"]["page_info"]

            # If a next page of results exists
            if (pageInfo["has_next_page"]):
                cursor = facebookResponse["data"]["marketplace_search"]["feed_units"]["page_info"]["end_cursor"]

                # Make a copy of the original request payload
                requestPayloadCopy = copy.copy(requestPayload)

                # Insert the cursor object into the variables object of the request payload copy
                requestPayloadCopy["variables"] = requestPayloadCopy["variables"].split(
                )
                requestPayloadCopy["variables"].insert(
                    1, """"cursor":'{}',""".format(cursor))
                requestPayloadCopy["variables"] = "".join(
                    requestPayloadCopy["variables"])

                status, error, facebookResponse = getFacebookResponse(
                    requestPayloadCopy)

                if (status == "Success"):
                    facebookResponse = json.loads(facebookResponse.text)
                    rawPageResults.append(facebookResponse)
                else:
                    return (status, error, data)
    else:
        return (status, error, data)

    # Parse the raw page results and set as the value of listingPages
    data["listingPages"] = parsePageResults(rawPageResults)
    return (status, error, data)

def get_listing_description(id):
    variables = {
        'targetId': id,
        'UFI2CommentsProvider_commentsKey': 'MarketplacePDP',
        'canViewCustomizedProfile': 'true',
        'feedbackSource': '56',
        'feedLocation': 'MARKETPLACE_MEGAMALL',
        'location_vanity_page_id': '107286902636860',
        'pdpContext_isHoisted': 'false',
        'pdpContext_trackingData': 'browse_serp:ab93c14a-095b-445c-850f-89e2566c9a3d',
        'referralCode': 'null',
        'relay_flight_marketplace_enabled': 'false',
        'removeDeprecatedCommunityRecommended': 'true',
        'scale': '2',
        'should_show_new_pdp': 'false',
        'useDefaultActor': 'false' }
    requestPayload = {
        'variables': str(json.dumps(variables)),
        'doc_id': '5516791808425679'
    }
    
    '''{"UFI2CommentsProvider_commentsKey":"MarketplacePDP","canViewCustomizedProfile":true,"feedbackSource":56,"feedLocation":"MARKETPLACE_MEGAMALL","imageContext":"mp_comet_webp","location_latitude":40.4016,"location_longitude":-74.3063,"location_radius":16,"location_vanity_page_id":"108675425831191","pdpContext_isHoisted":false,"pdpContext_trackingData":"browse_serp:9738f95a-5679-4285-8509-694275bdd81a","referralCode":"null","relay_flight_marketplace_enabled":false,"scale":1.5,"should_show_new_pdp":false,"targetId":"539507251483653","useDefaultActor":false,"__relay_internal__pv__StoriesRingrelayprovider":false}'''
    
    status, error, facebookResponse = getFacebookResponse(requestPayload)
    return facebookResponse['data']['viewer']['marketplace_product_details_page']['target']['redacted_description']['text']
    
def find_site(requestPayload, max_retry_count=3):
    count = 0
    while count < max_retry_count:
        try:
            facebookResponse = requests.post(
                GRAPHQL_URL, headers=GRAPHQL_HEADERS, data=requestPayload, timeout=15)
            return facebookResponse
        except requests.exceptions.RequestException:
            print("Request error, giving it 10 and retrying")
            time.sleep(10)
            count += 1
    return None

# Helper function
def getFacebookResponse(requestPayload):
    status = "Success"
    error = {}

    # Try making post request to Facebook, excpet return
    facebookResponse = find_site(requestPayload)
    if (facebookResponse.status_code == 200):
        responseText = facebookResponse.text
        facebookResponseJSON = json.loads(responseText)
        return ("Success", error, facebookResponseJSON)
    else:
        status = "Failure"
        error["source"] = "Facebook"
        error["message"] = "Status code {}".format(
            facebookResponse.status_code)

    return (status, error, facebookResponse)


# Helper function
def parsePageResults(rawPageResults):
    listingPages = []

    pageIndex = 0
    
    for rawPageResult in rawPageResults:

        # Create a new listings object within the listingPages array
        listingPages.append({'listings': []})

        for listing in rawPageResult['data']['marketplace_search']['feed_units']['edges']:

            # If object is a listing
            if (listing['node']['__typename'] == 'MarketplaceFeedListingStoryObject'):
                print(json.dumps(listing, indent=4))
                listingID = listing['node']['listing']['id']
                listingName = listing['node']['listing']['marketplace_listing_title']
                listingCurrentPrice = listing['node']['listing']['listing_price']['formatted_amount']

                # If listing has a previous price
                if (listing['node']['listing']['strikethrough_price']):
                    listingPreviousPrice = listing['node']['listing']['strikethrough_price']['formatted_amount']
                else:
                    listingPreviousPrice = ''

                listingSaleIsPending = listing['node']['listing']['is_pending']
                listingPrimaryPhotoURL = listing['node']['listing']['primary_listing_photo']['image']['uri']
                sellerName = listing['node']['listing']['marketplace_listing_seller']['name']
                sellerLocation = listing['node']['listing']['location']['reverse_geocode']['city_page']['display_name']

                # Add the listing to its corresponding page
                listingPages[pageIndex]['listings'].append({
                    'title': listingName,
                    'description': get_listing_description(listingID),
                    'currentPrice': listingCurrentPrice,
                    'previousPrice': listingPreviousPrice,
                    'saleIsPending': str(listingSaleIsPending).lower(),
                    'primaryPhotoURL': listingPrimaryPhotoURL,
                    'sellerName': sellerName,
                    'sellerLocation': sellerLocation
                })

        pageIndex += 1

    return listingPages

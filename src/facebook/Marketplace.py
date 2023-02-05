from src import utils

from .MarketplaceLocationResponse import MarketplaceLocationResponse
from .MarketplaceSearchResponse import MarketplaceSearchResponse 

class Marketplace: 
    
    def get_locations(self, location_query: str) -> MarketplaceLocationResponse:
        '''
        Gets the Facebook location data associated with a location, passed in as a string

        Parameters:
        location_query (string): Any location, passed in as a string (ex. "Los Angeles", "90210")
        
        Returns:
        MarketplaceLocationResponse: Class that has a function `get_locations` that returns a list of locations 
            (dictionary of name, latitude, longitude)
        '''
        
        DOC_ID = "5585904654783609" # Honestly have no idea what these do, don't ask
        
        payload = {
            "variables": """{"params": {"caller": "MARKETPLACE", "page_category": ["CITY", "SUBCITY", "NEIGHBORHOOD","POSTAL_CODE"], "query": "%s"}}""" % (location_query),
            "doc_id": DOC_ID
        }
        print(payload)
        response = utils.post_request(payload)
        return MarketplaceLocationResponse(response)
        
    def get_listings(self, latitude: str, longitude: str, search_query: str) -> MarketplaceSearchResponse:
        '''
        Gets the Facebook listings for a given location and search query.
        NOTE: For each listing, this makes a call to the listing details API to retrieve timestamp and description. 
        Therefore, this call will take much longer than get_locations().

        Parameters:
        latitude (string): Any latitude
        longitude (string): Any longitude
        search_query (string): Any search query representation. Things like "free AND red" seem to work, but not sure how much nuance Facebook accepts.
        
        Returns:
        MarketplaceSearchResponse: Class that has a function `get_listings` that returns a list of listings 
            (dictionary of updatedTimeStamp, title, description, currentPrice, previousPrice, saleIsPending, primaryPhotoURL, sellerName, sellerLocation)
        '''
        print("Getting listings for query " + search_query)
        DOC_ID = "7111939778879383" # Honestly have no idea what these do, don't ask
        
        payload = {
            "variables": """{"count":24, "params":{"bqf":{"callsite":"COMMERCE_MKTPLACE_WWW","query":"%s"},"browse_request_params":{"commerce_enable_local_pickup":true,"commerce_enable_shipping":true,"commerce_search_and_rp_available":true,"commerce_search_and_rp_condition":null,"commerce_search_and_rp_ctime_days":null,"filter_location_latitude":%s,"filter_location_longitude":%s,"filter_price_lower_bound":0,"filter_price_upper_bound":214748364700,"filter_radius_km":16},"custom_request_params":{"surface":"SEARCH"}}}""" % (search_query, latitude, longitude),
            "doc_id": DOC_ID
        }
        
        response = utils.post_request(payload)
        return MarketplaceSearchResponse(response, search_query).get_listings()
        

import json

class MarketplaceLocationResponse:
    
    def __init__(self, response):
        if (response.status_code != 200):
            raise ValueError(response.text)
        try:
            response_json = json.loads(response.text)
            self.create_locations(response_json)
        except ValueError as e:
            raise ValueError(e.message)
        
    def create_locations(self, response):
        self.locations = []
        try:
            data = response["data"]["city_street_search"]["street_results"]["edges"]
        except KeyError as ke:
            raise ValueError("ERROR: Invalid response from get_locations. Please try again with a different location string.", ke)
        for node in data:
            
            location_name = node["subtitle"].split(" \u00b7")[0]

            # Refine location name if it is too general
            if (location_name == "City"):
                location_name = node["single_line_address"]

            location_latitude = node["location"]["latitude"]
            location_longitude = node["location"]["longitude"]
            
            self.locations.append({
                "name": location_name,
                "latitude": str(location_latitude),
                "longitude": str(location_longitude)
            })
            
    def get_locations(self):
        return self.locations
    
class MarketplaceSearchResponse:
    
    def __init__(self, response):
        if (response.status_code != 200):
            raise ValueError(response.text)
        try:
            response_json = json.loads(response.text)
            self.create_listings(response_json)
        except ValueError as e:
            raise ValueError(e.message)
    
    def create_listings(self, response):
        return response
        
    def get_listings(self):
        return self.listings

from src import utils

class Marketplace: 
    
    API_URL = "https://www.facebook.com/api/graphql/"
    HEADERS = {
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"
}
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
        
        response = utils.post_request(self.API_URL, self.HEADERS, payload)
        return MarketplaceLocationResponse(response)
        
    def get_listings(self, latitude: str, longitude: str, search_query: str) -> MarketplaceSearchResponse:
        '''
        Gets the Facebook listings for a given location and search query.

        Parameters:
        latitude (string): Any latitude
        longitude (string): Any longitude
        search_query (string): Any search query representation. Things like "free AND red" seem to work, but not sure how much nuance Facebook accepts.
        
        Returns:
        MarketplaceSearchResponse: Class that has a function `get_listings` that returns a list of listings 
            (dictionary of updatedTimeStamp, title, description, currentPrice, previousPrice, saleIsPending, primaryPhotoURL, sellerName, sellerLocation)
        '''
        
        DOC_ID = "7111939778879383" # Honestly have no idea what these do, don't ask
        
        payload = {
            "variables": """{"count":24, "params":{"bqf":{"callsite":"COMMERCE_MKTPLACE_WWW","query":"%s"},"browse_request_params":{"commerce_enable_local_pickup":true,"commerce_enable_shipping":true,"commerce_search_and_rp_available":true,"commerce_search_and_rp_condition":null,"commerce_search_and_rp_ctime_days":null,"filter_location_latitude":%s,"filter_location_longitude":%s,"filter_price_lower_bound":0,"filter_price_upper_bound":214748364700,"filter_radius_km":16},"custom_request_params":{"surface":"SEARCH"}}}""" % (search_query, latitude, longitude),
            "doc_id": DOC_ID
        }
        
        response = utils.post_request(self.API_URL, self.HEADERS, payload)
        return MarketplaceSearchResponse(response)
        

from src import utils

from .MarketplaceLocationResponse import MarketplaceLocationResponse
from .MarketplaceSearchResponse import MarketplaceSearchResponse 

class Marketplace: 
    
    def __init__(self, latitude: str, longitude: str):
        self.latitude = latitude
        self.longitude = longitude
    
    def get_locations(self, location_query: str) -> MarketplaceLocationResponse:
        '''
        Gets the Facebook location data associated with a location, passed in as a string

        Parameters:
        location_query (string): Any location, passed in as a string (ex. "Los Angeles", "90210")
        
        Returns:
        MarketplaceLocationResponse: Class that has a function `get_locations` that returns a list of locations 
            (dictionary of name, latitude, longitude)
        '''
        
        DOC_ID = "6013160038790754" # Honestly have no idea what these do, don't ask
        
        payload = {
            "variables": """{"params": {"caller": "MARKETPLACE", "page_category": ["CITY", "SUBCITY", "NEIGHBORHOOD","POSTAL_CODE"], "query": "%s"}}""" % (location_query),
            "doc_id": DOC_ID
        }
        response = utils.post_request(payload)
        return MarketplaceLocationResponse(response)
        
    def get_listings(self, search_query: str, debug_mode=False,) -> MarketplaceSearchResponse:
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
        
        if (debug_mode):
            print("Getting listings for query " + search_query)
            
        DOC_ID = "7111939778879383" # Honestly have no idea what these do, don't ask

        payload = {
            "variables": self.get_search_variables(search_query),
            "doc_id": DOC_ID,
            "routing_namespace": "fb_comet",
            "__user": "0",
            "__a": "1",
            "__dyn": "7xeUmwlE7ibwKBWo2vwAxu13wvoKewSwMwNw9G2S0im3y4o0B-q1ew65xO0FE2awt81sbzoaEd82ly87e2l0Fwqo31wnEfo5m1mxe6E7e58jwGzEao4236222SUbElxm0zK5o4q0GpovU1aUbodEGdwko2QwbS1bw",
            "__req": "y",
            "__hs": "19072.HYP%3Acomet_loggedout_pkg.2.0.0.0.",
            "dpr": "1",
            "__ccg": "EXCELLENT",
            "__rev": "1005218752",
            "__s": "v7uzhb%3Awrp5dt%3Ar9ja1q",
            "__hsi": "7077666656081570639-0",
            "__comet_req": "1",
            "lsd": "AVp4CUdbFLA",
            "jazoest": "2876",
            "__spin_r": "1005218752",
            "__spin_b": "trunk",
            "__spin_t": "1647897683",
            "__csr": "hIIg-ySHYAR9qGGhml9HQqivGAuypWgF7CBl7Gl6KFonLgK8G9KayGUPJ5zAFQ79oCqfyoO5oiVVVVV4qVayorG4U4m4EsxKaxr-6polxF7UC8z9E88981jKU0mUw1SS0sOE099y00V7w0Czw0nPU0G-0zeh4ACwj86quqp2pe09UDypk5UB0by0E89o0swg5W2l2E27w2To0DC4E0i9w1h96wFw_w0yQxm9wiZm1JGm9giOwcm059U0bZ81do1l81cEmw1CWawioLwXCwfi"
        }
        response = utils.post_request(payload)
        if (debug_mode):
            print(response.text)
        return MarketplaceSearchResponse(response, search_query, debug_mode).get_listings()
    
    def get_search_variables(self, query):
            
            return """{
                "count" : 20,
                "params" : {
                    "bqf" : {
                        "callsite" : "COMMERCE_MKTPLACE_WWW",
                        "query" : "%s"
                    },
                    "browse_request_params" : {
                        "commerce_enable_local_pickup" : true,
                        "commerce_enable_shipping" : false,
                        "commerce_search_and_rp_available" : true,
                        "commerce_search_and_rp_condition" : null, 
                        "commerce_search_and_rp_ctime_days" : null,
                        "filter_location_latitude" : %s,
                        "filter_location_longitude" : %s,
                        "filter_price_lower_bound" : 0,
                        "filter_price_upper_bound" : 200,
                        "filter_radius_km":12,
                        "commerce_search_sort_by": "CREATION_TIME_DESCEND",
                    },
                    "custom_request_params" : {
                        "surface" : "SEARCH",
                        "search_vertical": "C2C"
                    }
                }
            }""" % (query, self.latitude, self.longitude)

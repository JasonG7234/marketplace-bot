import json

from .MarketplaceListingResponse import MarketplaceListingResponse
from src import utils

class MarketplaceSearchResponse:
    
    def __init__(self, response, query, debug_mode=False):
        self.query = query
        if (response.status_code != 200):
            raise ValueError(response.text)
        try:
            response_json = json.loads(response.text)
            self.response = response_json
            self.create_listings(response_json)
        except ValueError as e:
            raise ValueError(e)
    
    def create_listings(self, response, debug_mode=False):
        self.listings = []
        try:
            data = response['data']['marketplace_search']['feed_units']['edges']
        except KeyError:
            print(response)
            raise ValueError("ERROR: " + response['errors']['message'])
        
        for data_obj in data:
            node = data_obj['node']
            
            if (node['__typename'] == 'MarketplaceFeedListingStoryObject'):
                listing_id = node['listing']['id']
                listing_title = node['listing']['marketplace_listing_title']
                listing_current_price = node['listing']['listing_price']['formatted_amount']
                
                # If listing has a previous price
                if (node['listing']['strikethrough_price']):
                    listing_previous_price = node['listing']['strikethrough_price']['formatted_amount']
                else:
                    listing_previous_price = ''
                    
                listing_is_pending = node['listing']['is_pending']
                listing_photo_url = node['listing']['primary_listing_photo']['image']['uri']
                seller_name = node['listing']['marketplace_listing_seller']['name']
                seller_location = node['listing']['location']['reverse_geocode']['city_page']['display_name']
                
                if (debug_mode):
                    print("Getting listing details for listing id " + listing_id)
                listing_details = self.get_listing_details(listing_id)
                
                listing = {
                    'id' : listing_id,
                    'timestamp': listing_details.get_timestamp(),
                    'title': listing_title,
                    'description': listing_details.get_description(),
                    'currentPrice': listing_current_price,
                    'previousPrice': listing_previous_price,
                    'saleIsPending': str(listing_is_pending).lower(),
                    'condition': listing_details.get_condition(),
                    'primaryPhotoURL': listing_photo_url,
                    'category': self.query,
                    'sellerName': seller_name,
                    'sellerLocation': seller_location
                }
                
                self.listings.append(listing)
    
    def get_listing_details(self, listing_id):
        
        VARIABLES = {
            'targetId': listing_id,
            'UFI2CommentsProvider_commentsKey': 'MarketplacePDP',
            'canViewCustomizedProfile': 'true',
            'feedbackSource': '56',
            'feedLocation': 'MARKETPLACE_MEGAMALL',
            'pdpContext_isHoisted': 'false',
            'pdpContext_trackingData': 'browse_serp:ab93c14a-095b-445c-850f-89e2566c9a3d',
            'referralCode': 'null',
            'relay_flight_marketplace_enabled': 'false',
            'removeDeprecatedCommunityRecommended': 'true',
            'scale': '2',
            'should_show_new_pdp': 'false',
            'useDefaultActor': 'false' 
        }
        
        DOC_ID = "5516791808425679" # Honestly have no idea what these do, don't ask
        
        payload = {
            "variables": str(json.dumps(VARIABLES)), 
            "doc_id": DOC_ID
        }
        
        response = utils.post_request(payload)
        return MarketplaceListingResponse(response)
        
    def get_listings(self):
        return self.listings
    
    def __str__(self):
        return json.dumps(self.response, indent=4)
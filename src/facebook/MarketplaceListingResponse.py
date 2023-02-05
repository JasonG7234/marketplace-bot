import json
from datetime import datetime

class MarketplaceListingResponse:

    def __init__(self, response):
        if (response.status_code != 200):
            
            raise ValueError(response.status_code, response.text)
        try:
            response_json = json.loads(response.text)
            self.response = response_json
            self.create_listing_details(response_json)
        except ValueError as e:
            raise ValueError(e.message)
        
    def create_listing_details(self, response):
        
        self.description = response['data']['viewer']['marketplace_product_details_page']['target']['redacted_description']['text']
        epoch_timestamp = response['data']['viewer']['marketplace_product_details_page']['target']['creation_time']
        self.timestamp = datetime.fromtimestamp(epoch_timestamp)
        details = response['data']['viewer']['marketplace_product_details_page']['target']
        self.condition = None
        try:
            attribute_data_list = details['attribute_data']
            for attribute in attribute_data_list:
                if (attribute['attribute_name'] == "Condition"):
                    self.condition = attribute['label']
                    break
        except KeyError:
            self.condition = None
        
    def get_timestamp(self):
        return self.timestamp
    
    def get_description(self):
        return self.description
    
    def get_condition(self):
        return self.condition
        
    def __str__(self):
        return json.dumps(self.response, indent=4)
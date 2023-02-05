import json

class MarketplaceLocationResponse:
    
    def __init__(self, response):
        
        if (response.status_code != 200):
            raise ValueError(response.text)
        try:
            print(response.text)
            response_json = json.loads(response.text)
            self.response = response_json
            self.create_locations(response_json)
        except Exception as e:
            raise ValueError(e.message)
        
    def create_locations(self, response):
        self.locations = []
        try:
            data = response["data"]["city_street_search"]["street_results"]["edges"]
        except KeyError as ke:
            raise ValueError("ERROR: Invalid response from get_locations. Please try again with a different location string. ", ke)
        
        for data_obj in data:
            node = data_obj['node']
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
    
    def __str__(self):
        return json.dumps(self.response, indent=4)

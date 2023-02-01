from flask import Flask, request
import MarketplaceScraper

API = Flask(__name__)

def locations(locationQuery):
    response = {}

    if (locationQuery):
        status, error, data = MarketplaceScraper.getLocations(
            locationQuery=locationQuery)
    else:
        status = "Failure"
        error["source"] = "User"
        error["message"] = "Missing required parameter"
        data = {}

    response["status"] = status
    response["error"] = error
    response["data"] = data

    return response

def search(locationLatitude, locationLongitude, listingQuery):
    response = {}

    if (locationLatitude and locationLongitude and listingQuery):
        status, error, data = MarketplaceScraper.getListings(
            locationLatitude=locationLatitude, locationLongitude=locationLongitude, listingQuery=listingQuery)
    else:
        status = "Failure"
        error["source"] = "User"
        error["message"] = "Missing required parameter(s)"
        data = {}

    response["status"] = status
    response["error"] = error
    response["data"] = data

    return response

yuh = search("40.4016", "-74.3063", "free")
listings = yuh["data"]["listingPages"][0]["listings"]
for listing in listings:
    print(listing)
    print("============================================")
# print(locations("Old Bridge, New Jersey"))

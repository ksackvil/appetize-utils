# Des: This file makes a request to Google Places API to collect information about restaurants
#       in the given radius centered around Downtown Vancouver

import requests
import time
from env import apiKey
from data_parser import parseJson
import os

# Description: This is a class the contains the details of a restaurant like Name,
#               address, phone, tags, rating and website.
class Restaurant:
    def __init__(self, name, address, phone, tags, rating, website, location, google_id, photos, hours):
        self.name = name
        self.address = address
        self.phone = phone
        self.tags = tags
        self.rating = rating
        self.website = website
        self.location = location
        self.google_id = google_id
        self.photos = photos
        self.hours = hours
    
    # Des: converts class to type dict
    def to_dict(self):
        return{'name': self.name, 'address': self.address, 'phone': self.phone,
            'tags': self.tags, 'rating': self.rating, 'website': self.website, 'location': self.location, 'google_id': self.google_id, 'photos': self.photos, 'hours': self.hours}


def getImages(inputFile):
    photoCount = 0
    paths = inputFile.split('/')
    OUTPUT_FOLDER = ''

    for i in range(0,len(paths)-1):
        OUTPUT_FOLDER += paths[i]+'/'

    OUTPUT_FOLDER += 'images/'

    # create subfolder if it DNE
    if not os.path.exists(OUTPUT_FOLDER):
        os.mkdir(OUTPUT_FOLDER)

    KEY = apiKey()
    URLBASE = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&key='+KEY+'&photoreference='

    images = parseJson(inputFile)

    for image in images:
        google_id = image['google_id']
        
        # create subfolder if it DNE
        for ref in image['photo_reference']:
            if not os.path.exists(OUTPUT_FOLDER+google_id+'_'+ref[0:150]+'.png'):
                with open(OUTPUT_FOLDER+google_id+'_'+ref[0:150]+'.png', 'wb') as handle:
                    resp = requests.get(URLBASE+ref)

                    if not resp.ok:
                        print(resp)

                    else:
                        handle.write(resp.content)
                        photoCount+=1

            else:
                print('skip')                   

    return photoCount

#Des: # makes a request to Google Places API to collect information about restaurants
#        in the given radius centered around Downtown Vancouver
#Pre: location is a formatted string with 'long, lat' and radius is the distance in meters as a string
#Post: returns a list of type 'Restaurant' that contains all the restaurants
def getData(location, radius):
    #Location, radius and type of maps API search
    # Center point longitude, latitude
    LOCATION = location
    RAD = radius  # Radius distance in meters
    # Type of place we are searching for
    TYPE = 'restaurant'
    # My API key
    KEY = apiKey()

    # URL base for nearby search api call
    URLBASE = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?&key='+KEY

    # URL base for details search
    DETAILSURL = 'https://maps.googleapis.com/maps/api/place/details/json?&key='+KEY

    nearby_search = URLBASE+'&location='+LOCATION+'&radius='+RAD+'&type='+TYPE
    page_token = ''
    next_page = False

    r = requests.get(nearby_search)
    results = r.json()

    # If the key 'next_page_token' exists in our results then there is another page to our
    # query, must call for next page, update next_page to true so that we grab page token and store
    # this token in page_token
    if 'next_page_token' in results:
        next_page = True
        page_token = results['next_page_token']

    restaurantList = []     #List of type class Restaurant to store all restaurant search results

    # iterate through all the places in the query result, and store the desired keys in local
    # variable
    for place in results['results']:
        try:
            details = requests.get(DETAILSURL+'&placeid='+place['place_id'])
        except:
            details = ''

        try:
            name = details.json()['result']['name']
        except:
            name = ''

        try:
            address = details.json()['result']["formatted_address"]
        except:
            address = ''

        try:
            rating = details.json()['result']['rating']
        except:
            rating = ''

        try:
            phone = details.json()['result']['international_phone_number']
        except:
            phone = ''

        try:
            tags = details.json()['result']['types']
        except:
            tags = ''

        try:
            website = details.json()['result']['website']
        except:
            website = ''

        try:
            location = details.json()['result']['geometry']['location']
        except:
            location = {}

        try:
            google_id = details.json()['result']['place_id']
        except:
            google_id = ''

        try:
            photos = details.json()['result']['photos']
        except:
            photos = ''

        try:
            hours = details.json()['result']['opening_hours']['periods']
        except:
            hours = ''
        
        #append the restaurant to the list
        restaurantList.append(Restaurant(name, address, phone, tags, rating, website, location, google_id, photos, hours))

        #check the status of the result
        #print(details.json()['status'])

    # #Print results to screen
    # for restaurant in restaurantList:
    #     print("     ", restaurant.name, "            ", restaurant.address, "           ", restaurant.phone, "          ", restaurant.rating, "         ", restaurant.website)


    #check for new page
    # While there is a next page make another requests to fetch the next page of our
    # search result
    while next_page:

        # API call buffer
        time.sleep(2)

        r = requests.get(URLBASE+'&pagetoken='+page_token)
        results = r.json()

        # print('~~~~~~~~~~ new page ~~~~~~~~~~')

        # iterate through all the places in the query result, and store the desired keys in local
        # variable
        for place in results['results']:
            try:
                details = requests.get(DETAILSURL+'&placeid='+place['place_id'])
            except:
                details = ''

            try:
                name = details.json()['result']['name']
            except:
                name = ''

            try:
                address = details.json()['result']["formatted_address"]
            except:
                address = ''

            try:
                rating = details.json()['result']['rating']
            except:
                rating = ''

            try:
                phone = details.json()['result']['international_phone_number']
            except:
                phone = ''

            try:
                tags = details.json()['result']['types']
            except:
                tags = ''

            try:
                website = details.json()['result']['website']
            except:
                website = ''

            try:
                location = details.json()['result']['geometry']['location']
            except:
                location = {}

            try:
                google_id = details.json()['result']['place_id']
            except:
                google_id = ''

            try:
                photos = details.json()['result']['photos']
            except:
                photos = ''

            try:
                hours = details.json()['result']['opening_hours']['periods']
            except:
                hours = ''


            #append the restaurant to the list
            restaurantList.append(Restaurant(name, address, phone, tags, rating, website, location, google_id, photos, hours))

        # If the key 'next_page_token' exists in our results then there is another page to our
        # query, must call for next page, update next_page to true so that we grab page token and store
        # this token in page_token
        if 'next_page_token' in results:
            next_page = True
            page_token = results['next_page_token']
        else:
            # print('~~~~~ no more results ~~~~~')
            next_page = False
            break


    # #Print results to screen
    # for restaurant in restaurantList:
    #     print("     ", restaurant.name, "            ", restaurant.address, "           ", restaurant.phone, "          ", restaurant.rating, "         ", restaurant.website)
    return restaurantList
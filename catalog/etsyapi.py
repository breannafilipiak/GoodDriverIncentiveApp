import requests
import urllib.parse
import json

# A class that will contain all of the functionalities regarding the Etsy API.
#  Used to build, access, and alter catalog entries.

class EtsyAPI:

    """
    Class constructor
    
    params:
        - limit (optional), int: sets the default number of search results for
            the search function
    """
    def __init__(self, limit=10):
        
        # attempt authorization
        try:

            # read data from the auth.json file (private) and load into class
            with open('./auth.json') as f:
                data = json.load(f)
                self.keystring = data['etsy'][0]
                self.secret = data['etsy'][1]
        
        # throw authorization error
        except:
            print("Authorization error")
            return

        # assign laziness constants
        self.base_url = "https://openapi.etsy.com/v2/listings"
        self.api_key = "?api_key=" + self.keystring
        self.fields_arg = "&fields=title,description,price,currency_code"



    """
    function to search Etsy with a particular keyword
    
    params: 
        - keyword, str: the search term/phrase
        - limit, (optional) int: the number of search results to display
    
    returns:
        - a List containing the IDs returned by Etsy
    """
    def search(self, keyword, limit=10):

        # create list of listing IDs to return
        id_list = []

        # parse special characters (', ' ', etc)
        keyword = urllib.parse.quote(keyword)

        # generate GET url
        url = f"{self.base_url}/active{self.api_key}&limit={limit}&keywords={keyword}"
        
        # attempt GET request and retrieve data as JSON
        try:
            data = requests.get(url).json()
        except:
            print(f'GET request failed on keyword {keyword}')
            return

        # add found listing IDs to the list and return the list
        for id in data['results']:
            id_list.append(id['listing_id'])

        return id_list


    """
    function to retrieve metadata regarding a specific listing
    
    params:
        - ID, int: the ID of a listing (retrieved from EtsyAPI.search())
    
    returns:
        a Dictionary containing the listing data
        {
            "title"    : <string>
            "desc"     : <string>
            "price"    : <string>
            "currency" : <string>
        }
    """
    def getListing(self, ID):

        # results data dictionary
        results = {}

        # generate GET url
        listing_url = f"{self.base_url}/{ID}{self.api_key}{self.fields_arg}"
        
        # attempt GET request and retrieve data as JSON
        try:
            listing_data = requests.get(listing_url).json()
        except:
            print(f'GET request failed on ID {ID}')
            return

        # ugly chain of update statements to populate dictionary
        results.update({'title':listing_data['results'][0]['title']})
        results.update({'desc':listing_data['results'][0]['description']})
        results.update({'price':listing_data['results'][0]['price']})
        results.update({'currency':listing_data['results'][0]['currency_code']})


        return results


        
    """
    a function to get the images associated with a certain listing

    params:
        - ID, int: the listing ID for which to obtain the images

    returns:
        a List of image URLs posted with the listing
    """
    def getListingImg(self, ID):

        # generate GET url
        img_url = f"{self.base_url}/{ID}/images/{self.api_key}"

        # attempt GET request to obtain image data
        try:
            img_data = requests.get(img_url)
        except:
            print(f"GET request failed on image {ID}")
            return

        # generate and populate list of image URLs
        # using the 570 x N sizes
        result_urls = []

        for i in img_data.json()['results']:
            result_urls.append(i['url_570xN'])
        
        return result_urls

        
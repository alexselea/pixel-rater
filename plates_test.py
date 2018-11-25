import requests, json
import shutil
from urllib.request import urlopen
import os

from googleplaces import GooglePlaces, types, lang

from predict import run

def places(place_to_search):
    #private api ley
    API_KEY = 'AIzaSyDYgibuTAoQCBSQGRlR3UlHSy_vW00Q_yo'
    #the static url part of a text search query
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

    #read the name of the location
    query = place_to_search
    #the actual request
    r = requests.get(url + 'query=' + query + '&key=' + API_KEY)
    #convert it to a json
    x = r.json()
    #and access the results field
    y = x['results']
    #used for numbering the photos
    no = 1
    #only analyze the first result, can be modified by replacing range(1)
    query = query.replace(' ', '_')
    if os.path.exists('photos/' + query) == 0:
        os.mkdir('photos/' + query)

    for i in range(1):
        print(y[i]['name'])
        #the id of the location
        placeid = y[i]['place_id']
        #the static url part of a details query, used to request up to 10 images
        #relevant to said location
        place_url = 'https://maps.googleapis.com/maps/api/place/details/json?'
        place_r = requests.get(place_url + 'placeid=' + placeid + '&key=' + API_KEY)
        place_x = place_r.json()
        place_y = place_x['result']
        #access the photos field
        photos = place_y['photos']
        #for each photo
        for photo in photos:
            height = photo['height']
            width = photo['width']
            #the photo's id, used for fetching the actual image
            photo_reference = photo['photo_reference']
            #the static url part of a photo query
            photo_url = 'https://maps.googleapis.com/maps/api/place/photo?'
            photo_r = requests.get(photo_url +  'photoreference=' + photo_reference + '&maxwidth=' + str(width) +'&key=' + API_KEY)
            final_url = photo_url +  'photoreference=' + photo_reference + '&maxwidth=' + str(width) +'&key=' + API_KEY
            filename = "./photos/" + query + "/" + query + '_' + str(no) + '_image.jpg'
            no = no + 1
            f = open(filename, 'wb')
            #requesting the actual photo
            f.write(urlopen(final_url).read())
            f.close()

    print(run(place_to_search))
    


        
#time echo "maria ion regie" | python places_test.py 
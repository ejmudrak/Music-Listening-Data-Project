
# Reads in CSV file of username, college pairs for Campus Tunes study,
#   and assigns pair values to the data element of a json message and posts it to a url 

import sys, csv, requests, json
from collections import Counter 

# JSON Message, data initialized blank
json_data = {
    "customerId": "45c41088-135a-4105-8210-413d2218493e",
    "deviceId": "foo",
    "payload": {
        "type": "enroll",
        "version": 1,
        "pair": "",
        "lastfm": {
            "url": "No API call url found.",
            "data": "All API response data. None found."
        }
    }
}

## attributes of the api url for lastfm - some are done in the for loop
### method: (ex. user.getTopArtists, user.getTopAlbums, more at http://www.last.fm/api)
method = None
### period: (ex. overall, 12month, 6month, 1month, 7day)
period = None
### limit: # of items fetched (defaults to 50)
limit = 0

## Hardcoded values: 
# method = 'user.getTopArtists'
# ### period: (ex. overall, 12month, 6month, 1month, 7day)
# period = '1month'
# ### limit: # of items fetched (defaults to 50)
# limit = 100

### run python from inside of the lastfm-data folder!
## others: transy.csv, pairs_in.csv (for all), mudrak.csv (for single user)
PAIRS_IN = 'transy.csv'
PAIRS_OUT = 'pairs_out.csv'

print ("Lastfm data counting program:")

# Choose the method to print data 
methods = ['tracks', 'artists', 'albums']
method_input = None
while method_input not in methods:
    method_input = raw_input("Enter a method (ex. tracks, artists, albums): ")
    if method_input == "tracks":
        method = "user.getTopTracks"
    if method_input == "artists":
        method = "user.getTopArtists"
    if method_input == "albums":
        method = "user.getTopAlbums"
    if method_input not in methods:
        print "Method not recognized, try again."

# Choose the period of time that data will be accessed
periods = ["overall", "12month", "6month", "1month", "7day"]
while period not in periods:
    period = raw_input("Enter a time period (ex. overall, 12month, 6month, 1month, 7day): ")
    if period not in periods:
        print "Period not recognized, try again."

# Choose the limit, which decides the number of results per user
limit = raw_input("How many results do you want per user? (0 to 10,000): ")
    # if limit > 10000:
    #     print "Too large. Enter a number less than 10000"
    # if limit < 0:
    #     print "Enter a positive number"


fieldnames = ['username', 'college']
all_count = []

with open(PAIRS_IN, 'rb') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames, 'None', "None", delimiter=',', quotechar='|')
    for row in reader: 
        ### set pairs element to (username, college) pairs
        json_data['payload']['pair'] = row
        user = row['username']
        # Last.fm URL construction
        lastfm_url = "http://ws.audioscrobbler.com/2.0/?method=" + method + "&user=" + user + "&period=" + period + "&limit=" + str(limit) + "&api_key=57ee3318536b23ee81d6b27e36997cde&format=json"
        json_data['payload']['lastfm']['url'] = lastfm_url
        ### read in the lastfm user data by calling URL
        g = requests.get(lastfm_url).json()
        # calls URL as json, puts into data attr of json message
        json_data['payload']['lastfm']['data'] = g
        # shorten each json object based on the method being used, for our ease of use
        if method == "user.getTopTracks":
            lastfm_data = json_data['payload']['lastfm']['data']['toptracks']['track']
        if method == "user.getTopArtists":
            lastfm_data = json_data['payload']['lastfm']['data']['topartists']['artist']
        if method == "user.getTopAlbums": 
            lastfm_data = json_data['payload']['lastfm']['data']['topalbums']['album']

        ### Loop through data to print each song/artist/album result 
        # print user + "'s top list:
        user_count = []

        for index in range(len(lastfm_data)): 
            # Universal attributes:
            playcount = lastfm_data[index]['playcount']
            rank = lastfm_data[index]['@attr']['rank']

            if method == "user.getTopTracks":
                trackName = lastfm_data[index]['name']
                artistName = lastfm_data[index]['artist']['name']
                # Count the number of times a track is found in each user's data
                ## and add that tracks's name to a running total array 
                user_count.append(trackName)

                # Pretty print: 
                string = "\tAt Rank #" + rank + " is " + trackName + " by " + artistName + " with a playcount of " + playcount
                #print string
            if method == "user.getTopArtists":
                artistName = lastfm_data[index]['name']
                # Count the number of times an artist is found in each user's data
                ## and add that artist's name to a running total array
                user_count.append(artistName)

                # Pretty print
                string = "At Rank #" + rank + " is " + artistName + " with a playcount of " + playcount
                #print string
            if method == "user.getTopAlbums":
                albumName = lastfm_data[index]['name']
                artistName = lastfm_data[index]['artist']['name']
                user_count.append(albumName)
                string = "At Rank #" + rank + " is " + albumName + " by " + artistName + " with a playcount of " + playcount
                # print string 

            ### check for empty data:
            if not lastfm_data:
                print "/tThe user's listening history is empty!"
        ### Prints the count of each artist's occurence per user
        # print Counter(user_count)

        # Prints the count of each artists's occurence for all users
        ## by adding each user's array to an overall array
        ### of most common X results
        all_count.extend(user_count)
    counted = Counter(all_count).most_common(50)
    counter = 1
    for value, count in counted:
        print ("At #" + str(counter) + ":  " + value, count)
        counter = counter + 1

print("DONE")
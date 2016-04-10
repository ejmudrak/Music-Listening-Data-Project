
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
method = "user.getTopArtists"
method = None
### period: (ex. overall, 12month, 6month, 1month, 7day)
period = None
### limit: # of items fetched (defaults to 50)
limit = 0

### Hardcoded values: 
# method = 'user.getTopTracks'
# ### period: (ex. overall, 12month, 6month, 1month, 7day)
# period = 'overall'
# ### limit: # of items fetched (defaults to 50)
# limit = 25

### run python from inside of the lastfm-data folder!
PAIRS_IN = 'transy.csv'
PAIRS_OUT = 'pairs_out.csv'

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
            lastfm_data = json_data['payload']['lastfm']['data']['topalbums']['album']

        ### Loop through data to print each song/artist/album result 
        print user + "'s top list:"
        for index in range(len(lastfm_data)): 
            
            # Count the number of times an artist is found in each user's data
            # a = lastfm_data[index]
            # c = Counter(a['artist']['name'])
            # print(c)

            if method == "user.getTopTracks":
                trackName = lastfm_data[index]['name']
                artistName = lastfm_data[index]['artist']['name']
                playcount = lastfm_data[index]['playcount']
                rank = lastfm_data[index]['@attr']['rank']
                trackStr = "\tAt Rank #" + rank + " is " + trackName + " by " + artistName + " with a playcount of " + playcount
                print trackStr
            if method == "user.getTopArtists":
                artistName = lastfm_data[index]['name']
                playcount = lastfm_data[index]['playcount']
                rank = lastfm_data[index]['@attr']['rank']
                artistStr = "At Rank #" + rank + " is " + artistName + " with a playcount of " + playcount
                print artistStr
            if method == "user.getTopAlbums":
                print "NOT DONE YET"
            ### check for empty data:
            if not lastfm_data:
                print "/tThe user's listening history is empty!"

        ### print ALL of the data to the console:
        #print json_data
        ### post all of the data to the given URL: (uncomment to post)
        #    r = requests.post("https://h2v756ntkg.execute-api.us-east-1.amazonaws.com/staging/messages", data = json.dumps(json_data))
        ### prints the updated json data to a csv file
        ## json.dumps(json_data) - old method
        # json.dumps(json_data)
        ### prints full json formatted data to txt file: 
        # with open('lastfm.txt', 'w') as outfile:
        #     # json.dump(json_data, outfile)
        #     json.dump(json_data, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
        # writer.writerow(row)
print("DONE")
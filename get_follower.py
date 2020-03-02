from requests_oauthlib import OAuth1Session
import json
import configparser

key_ini = configparser.ConfigParser()
key_ini.read('key.ini')
consumer_key = key_ini['DEFAULT']['con_key']
consumer_secret =key_ini['DEFAULT']['secret']
access_token =key_ini['DEFAULT']['token']
access_token_secret =key_ini['DEFAULT']['token_secret']
twitter = OAuth1Session(consumer_key,consumer_secret,access_token,access_token_secret) 
url = "https://api.twitter.com/1.1/followers/list.json"
req = twitter.get(url)

keys = ["id", "name", "screen_name", "description", "friends_count", "followers_count","following","profile_image_url_https"]

if req.status_code == 200:
    user_info = json.loads(req.text)
#    for tweet in user_info:
#        print(user_info)

    for user in user_info["users"]:
        result = {}
        
        for key in keys:
            result[key] = user[key]
            
        print(result)
        print("\n")

else:
    print("ERROR: %d" % req.status_code)
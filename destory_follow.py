import tweepy
from requests_oauthlib import OAuth1Session
import json
import configparser

key_ini = configparser.ConfigParser()
key_ini.read('key.ini')
consumer_key = key_ini['DEFAULT']['con_key']
consumer_secret =key_ini['DEFAULT']['secret']
access_token =key_ini['DEFAULT']['token']
access_token_secret =key_ini['DEFAULT']['token_secret']

# OAuth認証
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# APIのインスタンスを生成
api = tweepy.API(auth)

# フォロー解除
user=getfront
try:
    api.destroy_friendship(screen_name=user)
    print("フォローを解除しました")
except tweepy.error.TweepError:
    print("フォロー解除に失敗しました")
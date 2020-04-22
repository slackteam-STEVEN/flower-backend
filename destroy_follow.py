import tweepy
import json
import MySQLdb
from db import conn_f
from contextlib import closing

# 認証キーの設定
def destroy_follow(ck,cs,random_key,screen_name):

    with closing(conn_f()) as conn:
        with conn.cursor() as cursor:
            sql = 'SELECT access_token, access_token_secret FROM auth WHERE random_key= %s'
            cursor.execute(sql,(random_key,))
            token = cursor.fetchone()
    access_token = token[0]
    access_token_secret = token[1]
    # OAuth認証
    auth = tweepy.OAuthHandler(ck,cs)
    auth.set_access_token(access_token, access_token_secret)

    # APIのインスタンスを生成
    api = tweepy.API(auth)
    try:
        api.destroy_friendship(screen_name)
        return json.dumps({'status_code': 200 , 'message':'OK'})
    except tweepy.error.TweepError:
        return json.dumps({'status_code': 404 , 'message':'Error'})
    

import tweepy
import json
import MySQLdb
from db import conn_f
from flask import Flask, redirect, request

def get_follow(ck,cs):
    random_key = request.args.get('random_key','')
    with conn_f() as conn:
        with conn.cursor() as cursor:
            sql = 'SELECT access_token, access_token_secret,screen_name FROM auth WHERE random_key=%s'
            cursor.execute(sql,(random_key,))
            token = cursor.fetchone()
    access_token = token[0]
    access_token_secret = token[1]
    screen_name = token[2]

    user_info_keys = ["id", "name", "screen_name", "description", "friends_count", "followers_count","profile_image_url_https"]
    cursor = -1
    while cursor != 0:
        #岩崎さん作成時に行うからいらない？→結論いる
        auth = tweepy.OAuthHandler(ck,cs)
        #API申請で取得したキー入れる
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True) #認証
        #get_follow()の引数にIDを指定し、idに入れ込む→scree_name入れた
        itr = tweepy.Cursor(api.friends_ids, id=screen_name, cursor=cursor).pages()
        user_info_list = []
        for user_id in itr.next():
            try:
                user = api.get_user(user_id)
                #変数の初期化
                user_info = {} 
                for user_info_key in user_info_keys:
                    user_info[user_info_key] = user._json[user_info_key]
                user_info_list.append(user_info)
                #user_info_listにuser_infoを入れ込む
            except tweepy.error.TweepError as e:
                result = {"status_code":400}
                result = json.dumps(result)
                return result
            except ConnectionError as e:
                result = {"status_code":500}
                result = json.dumps(result)
                return result
        result = {"status_code":200,"context":user_info_list}
        result = json.dumps(result)
        return result
    

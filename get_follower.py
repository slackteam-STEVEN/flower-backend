import tweepy
import json
import MySQLdb
from db import conn_f
from contextlib import closing

def get_follower(ck,cs,random_key):

    with closing(conn_f()) as conn:
        with conn.cursor() as cursor:
            sql = 'SELECT access_token,access_token_secret,screen_name FROM auth WHERE random_key= %s'
            cursor.execute(sql,(random_key,))
            token = cursor.fetchone()
    access_token = token[0]
    access_token_secret = token[1]
    screen_name = token[2]
    user_info_keys = ['id', 'name', 'screen_name', 'description', 'friends_count', 'followers_count','following','profile_image_url_https',]
    cursor = -1
    while cursor != 0:
        # OAuthHandlerインスタンスの作成
        auth = tweepy.OAuthHandler(ck,cs)
        # API申請で取得したキー入れる
        auth.set_access_token(access_token, access_token_secret) 
        api = tweepy.API(auth, wait_on_rate_limit=True) #認証
        itr = tweepy.Cursor(api.followers_ids, id=screen_name, cursor=cursor).pages()
        user_info_list = []
        for follower_id in itr.next():
            try:
                user = api.get_user(follower_id)
                user_info = {}
                for user_info_key in user_info_keys:
                    user_info[user_info_key] = user._json[user_info_key]
                user_info_list.append(user_info)            # user_info_listにuser_infoを入れ込む
            except tweepy.error.TweepError as e:
                result = {'status_code':400 , 'message':'Error'}
                result = json.dumps(result)
                return result
            except ConnectionError as e:
                result = {'status_code':500 , 'message':'Error'}
                result = json.dumps(result)
                return result
        result = {'status_code':200 , 'message':'OK' , 'context':user_info_list}
        result = json.dumps(result)
        return result
    

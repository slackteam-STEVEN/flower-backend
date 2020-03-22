import tweepy
import json

def get_follow(access_token,secret_access_taken,consumer_key,consumer_secret):
    user_info_keys = ["id", "name", "screen_name", "description", "friends_count", "followers_count","profile_image_url_https"]
    cursor = -1
    while cursor != 0:
        auth = tweepy.OAuthHandler(access_token, secret_access_taken)
        #API申請で取得したキー入れる
        auth.set_access_token(consumer_key, consumer_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True) #認証
        itr = tweepy.Cursor(api.friends_ids, id='自分のアカウントID', cursor=cursor).pages()
        user_info_list = []
        for user_id in itr.next():
            try:
                user = api.get_user(user_id)
                #変数の初期化
                user_info = {} 
                for user_info_key in user_info_keys:
                    user_info[user_info_key] = user[user_info_key]
                user_info_list.append(user_info)            #user_info_listにuser_infoを入れ込む
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
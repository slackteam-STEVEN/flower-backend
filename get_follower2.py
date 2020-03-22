import tweepy
import json

def get_follower(access_token,secret_access_taken,consumer_key,consumer_secret):
    user_info_keys = ["id", "name", "screen_name", "description", "friends_count", "followers_count","following","profile_image_url_https",]
    cursor = -1
    while cursor != 0:
        auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
        #API申請で取得したキー入れる
        auth.set_access_token(access_token, secret_access_taken) 
        api = tweepy.API(auth, wait_on_rate_limit=True) #認証
        itr = tweepy.Cursor(api.followers_ids, id='karasukoee', cursor=cursor).pages()
        user_info_list = []
        for ufollower_id in itr.next():
            try:
                user = api.get_user(follower_id)
                print(user)
                user_info = {}
                for user_info_key in user_info_keys:
                    user_info[user_info_key] = user._json[user_info_key]
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
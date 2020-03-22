from flask import Flask, render_template
import configparser
import tweepy
import json

app = Flask(__name__)
key_ini = configparser.ConfigParser()
key_ini.read('key.ini')
consumer_key = key_ini['DEFAULT']['con_key']
consumer_secret =key_ini['DEFAULT']['secret']

def get_follow(access_token,secret_access_token,consumer_key,consumer_secret):
    user_info_keys = ["id", "name", "screen_name", "description", "friends_count", "followers_count","profile_image_url_https"]
    cursor = -1
    while cursor != 0:
        auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
        auth.set_access_token(access_token, secret_access_taken) #API申請で取得したキー入れる
        api = tweepy.API(auth, wait_on_rate_limit=True) #認証
        itr = tweepy.Cursor(api.friends_ids, id='karasukoee', cursor=cursor).pages()
        user_info_list = []
        for user_id in itr.next():
            try:
                user = api.get_user(user_id)
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

def get_follower(access_token,secret_access_token,consumer_key,consumer_secret):
    user_info_keys = ["id", "name", "screen_name", "description", "friends_count", "followers_count","following","profile_image_url_https"]
    cursor = -1
    while cursor != 0:
        auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
        #API申請で取得したキー入れる
        auth.set_access_token(access_token, secret_access_token) 
        api = tweepy.API(auth, wait_on_rate_limit=True) #認証
        itr = tweepy.Cursor(api.followers_ids, id='karasukoee', cursor=cursor).pages()
        user_info_list = []
        for follower_id in itr.next():
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
        
@app.route('/account_authentication',methods=['GET'])
def account_authentication():
    global anngou_key
    global anngou_secret_key
    access_taken = "認証"
    secret_access_taken = "認証"
    anngou_key = "test"
    anngou_secret_key = "test1"
    
    respose = "0"

    return respose

@app.route('/get_follow',methods=['GET'])
def get_follows():
    #anngou_key = request.args.get('anngou_key')
    #anngou_secret_key = request.args.get('anngou_secret_key')
    access_token = "922767128016560129-bwiDEY3RyqLQHE7UUljY6BPOWJCz032"
    secret_access_token = "02nGQMfiLmwZMdNTsyg8SRrqu5FOBYy2k8ZZkxGYHDFdD"
    follow_list = get_follow(access_token, secret_access_token, consumer_key, consumer_secret)
    return follow_list

@app.route('/get_follower',methods=['GET'])
def get_followers():
    #anngou_key = request.args.get('anngou_key')
    #anngou_secret_key = request.args.get('anngou_secret_key')
    access_token = "922767128016560129-bwiDEY3RyqLQHE7UUljY6BPOWJCz032"
    secret_access_token = "02nGQMfiLmwZMdNTsyg8SRrqu5FOBYy2k8ZZkxGYHDFdD"
    follower_list = get_follower(access_token, secret_access_token, consumer_key, consumer_secret)
    return follower_list

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
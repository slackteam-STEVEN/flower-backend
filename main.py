from flask import Flask, redirect, request
import configparser
import tweepy
import json
import uuid
from db import conn_f

app = Flask(__name__)

ck = "*********"
cs = "*********"
callback_url = "callbackURL"


@app.route('/access',methods=['POST','GET'])
#DBにすでにuser_idが存在する場合＝ランダム文字列を返す
#DBにuser_idが存在しない場合＝取得したredirectURLと作成したランダム文字列を返す
def access():
    #フロント側からscreen_name受け取る
    screen_name=request.form.get(screen_name)
    
    #screen_nameからuser_idを検索
    user=api.get.user(screen_name)
    user_id = user['user_id']
    
    conn = conn_f()
    cursor = conn.cursor()
    
    #user_idをDB内で検索
    sql = 'SELECT user_id FROM auth WHERE user_id = %s'
    
    #検索したuser_idがDBでヒットしたら、ペアのランダム文字列を返す（アクセストークンも取得済み想定）
    if cursor.execute(sql,(user_id,)) == 1:
        sql = 'SELECT random_key FROM auth WHERE user_id=%s'
        cursor.execute(sql,(user_id,))
        random_key = cursor.fetchone()
        
        conn.commit()
        # 接続を閉じる
        cursor.close()
        conn.close()
        
        return  json.dumps({"status_code": 200,"random_key" : random_key[0]})
    
    #user_idがDBにない場合は、user_id,screen_name,取得したrequest_token,作成したランダム文字列をDBへ格納する↓
    else:
        auth = tweepy.OAuthHandler(ck, cs, callback_url)
        try:
            redirect_url = auth.get_authorization_url()
            request_token = auth.request_token
            random_key = str(uuid.uuid4())

            sql = 'INSERT INTO auth (user_id,screen_name,request_token,random_key) VALUE (%s,%s,%s,%s)'
            cursor.execute(sql,(user_id,screen_name,request_token,random_key,))

            conn.commit()
            # 接続を閉じる
            cursor.close()
            conn.close()
        
        except tweepy.TweepError:
            print('Error! Failed to get request token.')
        
        #redirect_url(連携画面URL)とランダム文字列を返す
        result = { "redirect_url" : redirect_url, "random_key" : random_key }
        return json.dumps({"status_code": 200, "context": result })


@app.route("/register", methods=["GET"])
def register():
    auth = tweepy.OAuthHandler(ck, cs, callback_url)
    #callbackURLにアクセスする
    #予めDBに保存していたoauth_tokenと一致するレコードにverifierを保存する。
    # アクセスしたタイミングでフロントからoauth_verifier,ランダム文字列を取得する
    random_key = request.args.get("random_key", "")
    oauth_verifier = request.args.get("oauth_verifier", "")
    
    #DBに保存していたrequest_tokenを呼び出し、auth.request_tokenへ代入し直す
    sql = 'SELECT request_token FROM auth WHERE random_key_id=%s'
    cursor.execute(sql,(random_key,))
    request_token = cursor.fetchone()
    auth.request_token = request_token[0]
    
    #verifierを呼び出し、アクセストークンを取得

    auth.get_access_token(oauth_verifier)
    
    at = auth.access_token
    ats = auth.access_token_secret
    
    sql = 'UPDATE auth SET access_token = %s , access_token_secret = %s WHERE random_key = %s'
    cursor.execute(sql,(at,ats,random_key,)) 
    
    
    conn.commit()
    # 接続を閉じる
    cursor.close()
    conn.close()
    
    #topページへリダイレクト
    return redirect("http://127.0.0.1:8000/following")


@app.route('/get_follow',methods=['GET'])
def get_follows():
    #DBに保存されたランダム文字列をキーとして生データ（アクセストークン）を持ってくる
    access_token = 'SELECT  access_token auth WHERE random_key = %s'
    access_token_secret = 'SELECT  access_token_secret auth WHERE random_key = %s'
    follow_list = get_follow(access_token, access_token_secret)
    return follow_list

@app.route('/get_follower',methods=['GET'])
def get_followers():
    #DBに保存されたランダム文字列をキーとして生データ（アクセストークン）を持ってくる
    access_token = 'SELECT  access_token auth WHERE random_key = %s'
    access_token_secret = 'SELECT  access_token_secret auth WHERE random_key = %s'
    follower_list = get_follower(access_token, access_token_secret)
    return follower_list


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)

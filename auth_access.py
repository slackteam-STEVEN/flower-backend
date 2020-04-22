from flask import Flask, redirect, request
import configparser
import tweepy
import json
import ulid
import MySQLdb
from db import conn_f

# DBにすでにuser_idが存在する場合＝ランダム文字列を返す
# DBにuser_idが存在しない場合＝取得したredirectURLと作成したランダム文字列を返す
def auth_access(ck,cs):
    # フロント側からscreen_nameを受け取る
    screen_name = request.form.get('screen_name')
    callback_url = request.form.get('callback_url')

    # screen_nameからuser_idを検索
    auth = tweepy.OAuthHandler(ck, cs, callback_url)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    user = api.get_user(screen_name)
    user_id = str(user.id)
    
    conn = conn_f()
    with conn.cursor() as cursor:
        try:
            # user_idをDB内で検索
            sql = 'SELECT user_id FROM auth WHERE user_id = %s'
            # 検索したuser_idがDBでヒットしたら、ペアのランダム文字列を返す（アクセストークンも取得済み想定）
            if cursor.execute(sql,(user_id,)) == 1:
                try:
                    sql = 'SELECT random_key FROM auth WHERE user_id = %s'
                    cursor.execute(sql,(user_id,))
                    random_key = cursor.fetchone()

                    conn.commit()
                    
                    return json.dumps({'status_code': 200,'random_key' : random_key[0]})
                except MySQLdb.Error:
                    return json.dumps({'status_code':1002,'message' : 'MySQL error'})
            
            # user_idがDBにない場合は、user_id,screen_name,取得したrequest_token,作成したランダム文字列をDBへ格納する↓
            else:
                
                try:
                    redirect_url = auth.get_authorization_url()
                    request_token = auth.request_token
                    random_key = str(ulid.new())
                    
                    sql = 'INSERT INTO auth (user_id,screen_name,request_token,random_key) VALUE (%s,%s,%s,%s)'
                    cursor.execute(sql,(user_id,screen_name,request_token,random_key,))
                    conn.commit()
                    # 接続を閉じる
    
                except tweepy.TweepError:
                    return json.dumps({'status_code': 32 , 'message' : 'Error! Failed to get request token.'})
                
                except MySQLdb.Error:
                    return json.dumps({'status_code': 1002 , 'message' : 'MySQL error'})
                    
                # redirect_url(連携画面URL)とランダム文字列を返す
                result = {'redirect_url' : redirect_url, 'random_key' : random_key }
                return json.dumps({'status_code': 200, 'context': result })
        
        except MySQLdb.Error:
            return json.dumps({'status_code': 1002 , 'message' : 'MySQL error'})


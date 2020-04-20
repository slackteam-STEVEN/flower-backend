from flask import Flask, redirect, request
import tweepy
import json
from db import conn_f

def auth_register(ck,cs):
    callback_url = request.args.get('callback_url','')
    auth = tweepy.OAuthHandler(ck, cs, callback_url)
    # callbackURLにアクセスする
    # 予めDBに保存していたoauth_tokenと一致するレコードにverifierを保存する。
    # アクセスしたタイミングでフロントからoauth_verifier,ランダム文字列を取得する
    random_key = request.args.get('random_key', '')
    oauth_verifier = request.args.get('oauth_verifier', '')
    
    conn = conn_f()
    with conn.cursor() as cursor:
        try:
            # DBに保存していたrequest_tokenを呼び出し、auth.request_tokenへ代入し直す
            sql = 'SELECT request_token FROM auth WHERE random_key_id = %s'
            cursor.execute(sql,(random_key,))
            request_token = cursor.fetchone()
            auth.request_token = request_token[0]
            
            # verifierを呼び出し、アクセストークンを取得
            try:
                auth.get_access_token(oauth_verifier)
                
                at = auth.access_token
                ats = auth.access_token_secret
                
                sql = 'UPDATE auth SET access_token = %s , access_token_secret = %s WHERE random_key = %s'
                cursor.execute(sql,(at,ats,random_key,))
                conn.commit()
                # 接続を閉じる
            
            except tweepy.TweepError:
                return json.dumps({'status_code': 32 , 'message' : 'Error! Failed to get request token.'})
            
            except MySQLdb.Error:
                return json.dumps({'status_code': 1002 , 'message' : 'MySQL error'})
                
            # topページへリダイレクト
            return json.dumps({'status_code': 200 }) 
            
        except MySQLdb.Error:
            return json.dumps({'status_code': 1002 , 'message' : 'MySQL error'})
        
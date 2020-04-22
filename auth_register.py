from flask import Flask, redirect, request
import tweepy
import json
import MySQLdb
import ast
from db import conn_f

def auth_register(ck,cs):
    callback_url = request.form.get('callback_url')
    auth = tweepy.OAuthHandler(ck, cs, callback_url)
    # callbackURLにアクセスする
    # 予めDBに保存していたoauth_tokenと一致するレコードにverifierを保存する。
    # アクセスしたタイミングでフロントからoauth_verifier,ランダム文字列を取得する
    random_key = request.form.get('random_key')
    oauth_verifier = request.form.get('oauth_verifier')

    conn = conn_f()
    with conn.cursor() as cursor:
        try:
            # DBに保存していたrequest_tokenを呼び出し、auth.request_tokenへ代入し直す
            sql = 'SELECT request_token FROM auth WHERE random_key = %s'
            cursor.execute(sql,(random_key,))
            request_token = cursor.fetchone()
            request_token = ast.literal_eval(request_token[0])
            auth.request_token = request_token
            auth.request_token['oauth_token_secret'] = oauth_verifier
            
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
                return json.dumps({'status_code': 32 , 'message' : 'Error! Failed to get access token.'})
            
            except MySQLdb.Error:
                return json.dumps({'status_code': 1002 , 'message' : 'MySQL error'})
                
            # topページへリダイレクト
            return json.dumps({'status_code': 200 }) 
            
        except MySQLdb.Error:
            return json.dumps({'status_code': 1002 , 'message' : 'MySQL error'})
        
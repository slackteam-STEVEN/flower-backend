import tweepy
import json
import MySQLdb
from flask import Flask, redirect, request
from db import conn_f

# 認証キーの設定
def add_follow(ck,cs):
    random_key = request.form.get('random_key')
    conn = conn_f()
    cursor = conn.cursor()
    sql = 'SELECT access_token, access_token_secret FROM auth WHERE random_key = %s'
    cursor.execute(sql,(random_key,))
    token = cursor.fetchone()
    cursor.close()
    conn.close()
    access_token = token[0]
    access_token_secret = token[1]
    # OAuth認証
    auth = tweepy.OAuthHandler(ck,cs)
    auth.set_access_token(access_token, access_token_secret)
    screen_name = request.form.get('screen_name')
    # APIのインスタンスを生成
    api = tweepy.API(auth)
    try:
        api.create_friendship(screen_name)
        return json.dumps({'status_code': 200})
    except tweepy.error.TweepError:
        return json.dumps({'status_code':404})

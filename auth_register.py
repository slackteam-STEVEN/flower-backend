import tweepy
import json
import MySQLdb
import ast
from contextlib import closing
from db import conn_f

def auth_register(ck,cs,callback_url,random_key,oauth_verifier):

    auth = tweepy.OAuthHandler(ck, cs, callback_url)

    with closing(conn_f()) as conn:
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
                    
                
                except tweepy.TweepError:
                    return json.dumps({'status_code':32 , 'message' : 'Error! Failed to get access token.'})
                
                except MySQLdb.Error:
                    return json.dumps({'status_code':1002 , 'message' : 'MySQL error'})
                    
                # topページへリダイレクト
                return json.dumps({'status_code':200 , 'message':'OK'}) 
                
            except MySQLdb.Error:
                return json.dumps({'status_code': 1002 , 'message' : 'MySQL error'})
                

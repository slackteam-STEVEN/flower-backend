from flask import Flask, redirect, request
from flask_cors import CORS
import configparser
import tweepy
import json
import ulid
from db import conn_f

import auth_access
import auth_register
import get_follow
import get_follower
import add_follow
import destroy_follow


app = Flask(__name__)
CORS(app) 

key_ini = configparser.ConfigParser()
key_ini.read('key.ini')
ck = key_ini['ConsumerKey']['con_key']
cs = key_ini['ConsumerKey']['secret']


@app.route('/access',methods=['POST'])
def access():
    screen_name = request.form.get('screen_name')
    callback_url = request.form.get('callback_url')
    result = auth_access.auth_access(ck,cs,screen_name,callback_url)
    return result

@app.route('/register', methods=['POST'])
def register():
    callback_url = request.form.get('callback_url')
    random_key = request.form.get('random_key')
    oauth_verifier = request.form.get('oauth_verifier')
    result = auth_register.auth_register(ck,cs,callback_url,random_key,oauth_verifier)
    return result

@app.route('/get_follow',methods=['GET'])
def get_follows():
    random_key = request.args.get('random_key','')
    follow_list = get_follow.get_follow(ck,cs,random_key)
    return follow_list

@app.route('/get_follower',methods=['GET'])
def get_followers():
    random_key = request.args.get('random_key','')
    follower_list = get_follower.get_follower(ck,cs,random_key)
    return follower_list

@app.route('/add_follow',methods=['POST'])
def add_follows():
    random_key = request.form.get('random_key')
    screen_name = request.form.get('screen_name')
    add_follow_list = add_follow.add_follow(ck,cs,random_key,screen_name)
    return add_follow_list

@app.route('/destroy_follow',methods=['POST'])
def destroy_follows():
    random_key = request.form.get('random_key')
    screen_name = request.form.get('screen_name')
    destroy_follow_list = destroy_follow.destroy_follow(ck,cs,random_key,screen_name)
    return destroy_follow_list
    

if __name__ == '__main__':
    app.run(host='10.0.1.10', port=8000)

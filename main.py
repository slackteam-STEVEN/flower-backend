from flask import Flask, redirect, request
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

key_ini = configparser.ConfigParser()
key_ini.read('key.ini')
ck = key_ini['DEFAULT']['con_key']
cs = key_ini['DEFAULT']['secret']

@app.route('/access',methods=['POST'])
def access():
    result = auth_access.auth_access(ck,cs)
    return result

@app.route('/register', methods=['POST'])
def register():    
    result = auth_register.auth_register(ck,cs)
    return result

@app.route('/get_follow',methods=['GET'])
def get_follows():
    follow_list = get_follow.get_follow(ck,cs)
    return follow_list

@app.route('/get_follower',methods=['GET'])
def get_followers():
    follower_list = get_follower.get_follower(ck,cs)
    return follower_list

@app.route('/add_follow',methods=['POST'])
def add_follows():
    add_follow_list = add_follow.add_follow(ck,cs)
    return add_follow_list

@app.route('/destroy_follow',methods=['POST'])
def destroy_follows():
    destroy_follow_list = destory_follow.destroy_follow(ck,cs)
    return destroy_follow_list
    

if __name__ == '__main__':
    app.run(host='10.0.1.10', port=8000)

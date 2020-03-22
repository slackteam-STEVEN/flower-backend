from flask import Flask, render_template
import configparser

app = Flask(__name__)
key_ini = configparser.ConfigParser()
key_ini.read('key.ini')
consumer_key = key_ini['DEFAULT']['con_key']
consumer_secret =key_ini['DEFAULT']['secret']

@app.route('/account_authentication',methods=['GET'])
def account_authentication():
    access_taken = "認証"
    secret_access_taken = "認証"
    anngou_key = angou(access_taken)
    anngou_secret_key = angou(secret_access_taken) 
    respose = {"access_taken": anngou_key, "secret_access_taken": anngou_secret_key}
    return respose

@app.route('/get_follow',methods=['GET'])
def get_follow():
    anngou_key = request.args.get('anngou_key')
    anngouanngou_secret_key_key = request.args.get('anngou_secret_key')
    access_taken = angou_kaijyo(anngou_key)
    secret_access_taken = angou_kaijyo(anngou_secret_key)
    follow_list = get_follow(access_taken, secret_access_taken, consumer_key, consumer_secret)
    return follow_list

@app.route('/get_follower',methods=['GET'])
def get_follower():
    anngou_key = request.args.get('anngou_key')
    anngouanngou_secret_key_key = request.args.get('anngou_secret_key')
    access_taken = angou_kaijyo(anngou_key)
    secret_access_taken = angou_kaijyo(anngou_secret_key)
    follower_list = get_follow(access_taken, secret_access_taken, consumer_key, consumer_secret)
    return follower_list

@app.route('/add_follow',methods=['POST'])
def add_follow():
    anngou_key = request.args.get('anngou_key')
    anngouanngou_secret_key_key = request.args.get('anngou_secret_key')
    access_taken = angou_kaijyo(anngou_key)
    secret_access_taken = angou_kaijyo(anngou_secret_key)
    add_follow = get_follow(access_taken, secret_access_taken, consumer_key, consumer_secret)
    return add_follow

@app.route('/unfollow',methods=['POST'])
def unfollow():
     anngou_key = request.args.get('anngou_key')
    anngouanngou_secret_key_key = request.args.get('anngou_secret_key')
    access_taken = angou_kaijyo(anngou_key)
    secret_access_taken = angou_kaijyo(anngou_secret_key)
    destory_follow = get_follow(access_taken, secret_access_taken, consumer_key, consumer_secret)
    return destory_follow

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
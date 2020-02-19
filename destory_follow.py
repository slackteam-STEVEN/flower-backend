import tweepy

# 認証キーの設定
consumer_key = "2oNzJD7rceT2iWxhKxR9tSZPm"
consumer_secret = "zGCwDZ5ihlix0FFCEDJK5Yfza9j4IGm4uyQKOWpueakbBGoz1T"
access_token = "922767128016560129-JLi7KH5cUX52a8kJC8j5Bd8CJnPrPdY"
access_token_secret = "3cakJdDZGkdomVE3B5jmeUMp6xZlCElBfvlmTmeKvcUyi"

# OAuth認証
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# APIのインスタンスを生成
api = tweepy.API(auth)

# フォロー解除
user = input("「@ユーザー名」を入力してください：")
try:
    api.destroy_friendship(screen_name=user)
    print("フォローを解除しました")
except tweepy.error.TweepError:
    print("フォロー解除に失敗しました")
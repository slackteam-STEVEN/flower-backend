import tweepy

# 認証キーの設定
consumer_key = "2oNzJD7rceT2iWxhKxR9tSZPm"
consumer_secret = "zGCwDZ5ihlix0FFCEDJK5Yfza9j4IGm4uyQKOWpueakbBGoz1T"
access_token = "922767128016560129-4JOptNReRKKgAm3Mqc9XpmRySvBDKK8"
access_token_secret = "y943JxcecmHyTCuW2F4l3XYDa9Xopv4R7962LKZI3Qg6K"

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
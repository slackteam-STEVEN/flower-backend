import tweepy
cursor = -1
while cursor != 0:
    auth = tweepy.OAuthHandler("2oNzJD7rceT2iWxhKxR9tSZPm", 'zGCwDZ5ihlix0FFCEDJK5Yfza9j4IGm4uyQKOWpueakbBGoz1T')
    auth.set_access_token('922767128016560129-JLi7KH5cUX52a8kJC8j5Bd8CJnPrPdY','3cakJdDZGkdomVE3B5jmeUMp6xZlCElBfvlmTmeKvcUyi')
    api = tweepy.API(auth, wait_on_rate_limit=True)
    itr = tweepy.Cursor(api.friends_ids, id=input("＠以降のユーザー名を入力してください:"), cursor=cursor).pages()
    try:
        for user_id in itr.next():
            try:
                user = api.get_user(user_id)
                user_info = [user.id_str, user.screen_name, user.name,user.following,user.friends_count,user.followers_count,]
                print(user_info)
            except tweepy.error.TweepError as e:
                print(e.reason)
    except ConnectionError as e:
        print(e.reason)
    cursor = itr.next_cursor
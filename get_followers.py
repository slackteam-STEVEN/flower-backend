import tweepy
cursor = -1
while cursor != 0:
    auth = tweepy.OAuthHandler('2oNzJD7rceT2iWxhKxR9tSZPm','zGCwDZ5ihlix0FFCEDJK5Yfza9j4IGm4uyQKOWpueakbBGoz1T')
    auth.set_access_token('922767128016560129-hVgHBjb4xLTUonC4JEDE3dvY1sjMHQO','a54v2Eu19VucSWph3QyEekTI4kxpoClCKWD9tsTzCTnOG')
    api = tweepy.API(auth, wait_on_rate_limit=True)
    itr = tweepy.Cursor(api.followers_ids, id='noname0326', cursor=cursor).pages()
    try:
        for follower_id in itr.next():
            try:
                user = api.get_user(follower_id)
                user_info = [user.screen_name, user.name,user.description]
                print(user_info)
            except tweepy.error.TweepError as e:
                print(e.reason)
    except ConnectionError as e:
        print(e.reason)
    cursor = itr.next_cursor
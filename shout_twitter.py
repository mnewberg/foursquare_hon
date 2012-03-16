import tweepy
import settings

def send_twitter_shout(t_handle,message,uid):
    consumer_key=settings.CONSUMER_KEY
    consumer_secret=settings.CONSUMER_SECRET
    access_token=settings.ACCESS_TOKEN
    access_token_secret=settings.ACCESS_TOKEN_SECRET
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    try: 
        api.update_status(t_handle+' '+message+' http://staging.tryfourplay.com/message/'+ uid)
        success=True
    except:
        success=False
    return (success)

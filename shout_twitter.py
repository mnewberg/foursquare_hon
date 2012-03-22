import tweepy
import settings

consumer_key=settings.CONSUMER_KEY
consumer_secret=settings.CONSUMER_SECRET
access_token=settings.ACCESS_TOKEN
access_token_secret=settings.ACCESS_TOKEN_SECRET
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def send_twitter_shout(t_handle,sender,venue_name,uid):
    try: 
        api.update_status(t_handle+' '+'Hey!'+ sender+' saw you check-in @ '+ venue_name +' & left you a message. See who it was here http://staging.tryfourplay.com/message/'+ uid)
        success=True
    except:
        success=False
    return (success)

def get_bio(t_handle):
    user=api.get_user(t_handle)
    bio=user.description.strip('\r\n')
    location=user.location
    return location, bio


import tweepy
import settings
import random
import logging

logger=logging.getLogger(settings.LOGGER_ID)

consumer_key=settings.CONSUMER_KEY
consumer_secret=settings.CONSUMER_SECRET
access_token=settings.ACCESS_TOKEN
access_token_secret=settings.ACCESS_TOKEN_SECRET
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def send_twitter_shout(t_handle,sender,f_name,venue_name,uid):
    options=[('@'+t_handle+' '+'Yo '+f_name+'! This is crazy but '+ sender+' just saw you check-in @ '+ venue_name +' & challenged you to a game of trivia: http://playdo.pe/message/'+ uid),('@'+t_handle+' '+'Hey '+f_name+'! This is crazy but '+ sender +' just saw you check-in @ '+ venue_name +' & challenged you to a game of trivia: http://playdo.pe/message/'+ uid),('@'+t_handle+' '+'Hey '+f_name+'!'+ sender+' is around the corner from your check-in @ '+ venue_name +' & challenged you to a game of trivia: http://playdo.pe/message/'+ uid)]
    try: 
        api.update_status(random.choice(options))
        success=True
    except:
        success=False
        logger.error('There was a twitter error', exc_info=True, extra={'stack': True})
    return (success)

def get_bio(t_handle):
    try:
        user=api.get_user(t_handle)
        bio=user.description.strip('\r\n')
        location=user.location
        return location, bio
    except:
        return ''

import bitly_api
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

bitly_key='R_4d6d45ada0e0b63358e51af5161c0074'
bitly_user='thenewb'

bitly=bitly_api.Connection(bitly_user,bitly_key)


def send_twitter_shout(t_handle,sender,f_name,venue_name,uid):
    url=str(bitly.shorten('http://playdo.pe/'+uid))
    options=[('@'+t_handle+' '+'Yo '+f_name+'! This is crazy but '+ sender+' just saw you check-in @ '+ venue_name +' & challenged you to a game of trivia: '+ url),('@'+t_handle+' '+'Hey '+f_name+'! This is crazy but '+ sender +' just saw you check-in @ '+ venue_name +' & challenged you to a game of trivia: '+ url),('@'+t_handle+' '+'Hey '+f_name+'! '+ sender+' is around the corner from your check-in @ '+ venue_name +' & challenged you to a game of trivia: '+ url)]
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

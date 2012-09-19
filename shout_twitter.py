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


def send_twitter_shout(t_handle,sender,f_name,venue_name,uid,sender_twitter):
    url=str(bitly.shorten('http://playdo.pe/message/'+uid)['url'])
    if len(venue_name)>15:
        venue_name=[' '.join(venue_name.split(' ')[:2])][0]
    else:
        pass
    options=[('@'+t_handle+' '+'Yo '+f_name+'! This is crazy but @'+ sender_twitter +' just saw you checkin @ '+ venue_name +' & challenged you to a trivia game: '+ url),('@'+t_handle+' '+'Hey '+f_name+'! This is crazy but @'+ sender_twitter +' just saw you checkin @ '+ venue_name +' & challenged you to a trivia game: '+ url),('@'+t_handle+' '+'Hey '+f_name+'! @'+ sender_twitter+' is around the corner from you @ '+ venue_name +' & challenged you to a trivia game: '+ url)]
    choice=random.choice(options)
    if len(choice)>140:
        choice=('@'+t_handle+' Hey '+f_name+'! @'+sender_twitter+' is near '+venue_name+' & challenged you to a trivia game: '+url)
    else:
        pass
    try:
        api.update_status(choice)
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

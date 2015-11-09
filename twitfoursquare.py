import tweepy
import pysq.apiv2 as psq
import bitly_api
import re
import settings

bitly_key='R_4d6d45ada0e0b63358e51af5161c0074'
bitly_user='thenewb'

bitly=bitly_api.Connection(bitly_user,bitly_key)

authenticator = psq.FSAuthenticator(settings.CLIENT_ID, settings.CLIENT_SECRET, settings.CALLBACK_URL)


consumer_key=settings.CONSUMER_KEY
consumer_secret=settings.CONSUMER_SECRET
access_token=settings.ACCESS_TOKEN
access_token_secret=settings.ACCESS_TOKEN_SECRET
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

pusher.app_id='19318'
pusher.key='890abd57f862ab2712ff'
pusher.secret='00d5dd3756b1594826f2'

@postpone
def nearby(the_id,lat,lon):
	u=user.object.get(fsq_id=the_id)
	token=u.token
	for i in api.search(geocode=lat+','+lon+',1mi',rpp='100',page=1,q='4sq.com',include_entities='true'):
		dalist=[]
		chickpix={}
		d=bitly.expand(shortUrl=i.entities['urls'][0]['expanded_url'])[0]['long_url']
		try:
			signature=re.findall('\^?s=.{27}',d)[0][2:]
		    checkin=re.findall('checkin/.{0,24}',d)[0][8:]
			entry=authenticator.query('/checkins/'+checkin,token,{'signature':signature})
			p['chickpix-'+token].trigger('done','')
			fname=entry['user']['firstName']
			fsq_id=entry['user']['id']
			pic_id=entry['user']['photo'][36:]
			twitter=entry['user']['contact']['twitter']
			venue_id=entry['checkin']['venue']['id']
			venue_name=entry['checkin']['venue']['name']
			chickpix[fsq_id]=[pic_id,fname,venue_name.split('-')[0],venue_id,twitter]
			p['chickpix-'+token].trigger('image',{'entry':chickpix[fsq_id]})
			try:
	            user_lookup.objects.create(first_name=fname,fsq_id=fsq_id,pic_id=pic_id,t_handle=twitter)
			except:
				pass
		except:
				pass
		return 'Ok'
		
	
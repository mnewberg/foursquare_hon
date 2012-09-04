import pysq.apiv2 as psq
from categorize import *
import settings
from randomizer import chunk
from django.shortcuts import render_to_response
from gallery.models import *
import tweepy
import simplejson
from django.http import HttpResponse
import pusher
from pyklout import Klout
from background import postpone
import bitly_api
import re
import logging
from django.contrib.sessions.backends.db import SessionStore

logger=logging.getLogger(settings.LOGGER_ID)

consumer_key=settings.CONSUMER_KEY
consumer_secret=settings.CONSUMER_SECRET
access_token=settings.ACCESS_TOKEN
access_token_secret=settings.ACCESS_TOKEN_SECRET
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

authenticator = psq.FSAuthenticator(settings.CLIENT_ID, settings.CLIENT_SECRET, settings.CALLBACK_URL)
finder = psq.UserFinder(authenticator)

bitly_key='R_4d6d45ada0e0b63358e51af5161c0074'
bitly_user='thenewb'

bitly=bitly_api.Connection(bitly_user,bitly_key)

pusher.app_id='19318'
pusher.key='890abd57f862ab2712ff'
pusher.secret='00d5dd3756b1594826f2'



# def newgallery(request):
#     bigdict={}
#     lat=request.GET['lat']
#     lon=request.GET['lon']
#     for i in range(1,16):
#         d=api.search(geocode=lat+','+lon+',1mi',rpp='100',page=i)
#         for result in d:
#             if result in bigdict:
#                 pass
#             else:
#                 bigdict[result.from_user_id]=re.sub('_normal','',result.profile_image_url)
#     return render_to_response('newgallery.html',{'bigdict':bigdict})


def ajaxreq(request):
	lat=request.GET['lat']
	lon=request.GET['lon']
	fsq_id=request.session['fsq_id']
	request.session['chickpix']=[]
	key=request.session.session_key
	new_nearby(key,fsq_id,lat,lon)
	return HttpResponse('OK!')
    
@postpone
def new_nearby(key,the_id,lat,lon):
	p = pusher.Pusher()
	p['error'].trigger('hit','')
	lat=str(lat)
	lon=str(lon)
	u=user.objects.get(fsq_id=the_id)
	token=u.token
	found=[]
	chickpix={}
	for i in api.search(geocode=lat+','+lon+',1mi',rpp='100',page=1,q='4sq.com',include_entities='true'):
		try: 
			d=bitly.expand(shortUrl=i.entities['urls'][0]['expanded_url'])[0]['long_url']
		except:
			logger.error('There was a bitly error', exc_info=True, extra={'stack': True,'url':i.text})
		if i.from_user not in found:
			if len(found)==10:
				p['chickpix-'+token].trigger('done','')
			else:
				pass
			try:
				signature=re.findall('\^?s=.{27}',d)[0][2:]
				checkin=re.findall('checkin/.{0,24}',d)[0][8:]
				entry=authenticator.query('/checkins/'+checkin,token,{'signature':signature})
				found.append(i.from_user)
				fname=entry['checkin']['user']['firstName']
				facebook=entry['checkin']['user']['contact']['facebook']
				fsq_id=entry['checkin']['user']['id']
				pic_id=entry['checkin']['user']['photo']
				if len(re.findall('blank',pic_id))>0:
					continue
				else:
					pic_id=pic_id[36:]
					pass
				twitter=i.from_user
				venue_id=entry['checkin']['venue']['id']
				venue_name=entry['checkin']['venue']['name']
				chickpix[fsq_id]=[pic_id,fname,venue_name.split('-')[0],venue_id,twitter]
				if len(found)<=10:
					p['chickpix-'+token].trigger('image',{'entry':chickpix[fsq_id]})
					if len(found)==1:
						s = SessionStore(session_key=key)
						s['chickpix']=[]
						s.save()
					else:
						pass
				else:
					try:
						s = SessionStore(session_key=key)
						s['chickpix'].append(chickpix[fsq_id])
						s.save()
					except:
						logger.error('chickpix',exc_info=True,extra={'stack':True,})
				try:
					user_lookup.objects.create(first_name=fname,fsq_id=fsq_id,facebook=facebook,pic_id=pic_id,t_handle=twitter)
				except:
					pass
			except:
				pass
		else:
			pass
	return 'Ok'


def get_page(request):
	d=request.session['chickpix'][:10]
	del request.session['chickpix'][:10]
	if request.session['chickpix']=='':
		done=True
	else:
		done=False
	return HttpResponse(simplejson.dumps({'d':d,'done':done}),mimetype='application/json')

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

bitly=bitly_api.bitly_api.Connection(bitly_user,bitly_key)

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
	new_nearby(fsq_id,lat,lon)
	return HttpResponse('OK!')
    
@postpone
def nearby(fsq_id,lat,lon):
    p = pusher.Pusher()
    u=user.objects.get(fsq_id=fsq_id)
    token = u.token
    trending=authenticator.query("/venues/trending", token, {'ll':str(lat)+','+str(lon)})
    trending_venues={}
    nearby_venues={}
    for item in trending['venues']:
        try:
            trending_venues[item['id']]=item['name']
        except:
            pass
    radius='2000'
    all_nearby = authenticator.query("/venues/search", token, {'ll':str(lat)+','+str(lon), 'limit':50, 'intent':'browse', 'radius':radius})
    i=0
    for item in all_nearby['venues']:
        if item['hereNow']['count']>0:
            nearby_venues[item['id']]=item['name']
    for item in set(nearby_venues).intersection(set(trending_venues)):
            del nearby_venues[item]
    all_venues_nearby = nearby_venues.items() + trending_venues.items()
    venue_names=[]
    chickpix={}
    backpix={}
    herenow=[]
    v_ids=[]
    i=0
    n=0


    for venue in all_venues_nearby:
            herenow.append(authenticator.query("/venues/"+venue[0]+"/herenow",token))
            v_ids.append(venue[0])
            herenow[i]['hereNow']['venueName']=venue[1][0]
            i = i+1
    p['chickpix-'+token].trigger('done','')
    for item in herenow:
            venueName=item['hereNow']['venueName']
            for entry in item['hereNow']['items']:
                  the_id=entry['user']['id']
                  query = finder.findUser(token, the_id)
                  twitter=query.twitter()
                  if entry['user']['photo'].startswith("https://foursquare.com/img/"):
                          pass
                  elif twitter:
                      chickpix[the_id]=[entry['user']['photo'][36:],entry['user']['firstName'],venueName.split('-')[0],v_ids[n],twitter]
                      p['chickpix-'+token].trigger('image',{'entry':chickpix[the_id]})                   
		      n+=1
                  try:
                      user_lookup.objects.create(first_name=entry['user']['firstName'],fsq_id=entry['user']['id'],pic_id=entry['user']['photo'][36:],t_handle=twitter)
                  except:
                      pass
    ## nobody nearby
    if n==0:
	    p['chickpix-'+token].trigger('crickets','')
    return 'Ok'

@postpone
def new_nearby(the_id,lat,lon):
	p = pusher.Pusher()
	p['error'].trigger('hit','')
	lat=str(lat)
	lon=str(lon)
	u=user.objects.get(fsq_id=the_id)
	token=u.token
	print token
	found=[]
	request.session['chickpix']={}
	for i in api.search(geocode=lat+','+lon+',1mi',rpp='100',page=1,q='4sq.com',include_entities='true'):
		d=bitly.expand(shortUrl=i.entities['urls'][0]['expanded_url'])[0]['long_url']
		print d
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
				chickpix={}
				fname=entry['checkin']['user']['firstName']
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
				request.session['chickpix'].append((fsq_id,chickpix[fsq_id]))
				#p['chickpix-'+token].trigger('image',{'entry':chickpix[fsq_id]})
				try:
					user_lookup.objects.create(first_name=fname,fsq_id=fsq_id,pic_id=pic_id,t_handle=twitter)
				except:
					pass
			except:
					p['chickpix-'+token].trigger('crickets','')
		else:
			pass
	return 'Ok'


def get_page(request):
	d=request.session[:10]
	del request.session[:10]
	return HttpResponse(simplejson.dumps({'d':d}),mimetype='application/json')

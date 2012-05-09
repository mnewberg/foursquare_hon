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

consumer_key=settings.CONSUMER_KEY
consumer_secret=settings.CONSUMER_SECRET
access_token=settings.ACCESS_TOKEN
access_token_secret=settings.ACCESS_TOKEN_SECRET
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

authenticator = psq.FSAuthenticator(settings.CLIENT_ID, settings.CLIENT_SECRET, settings.CALLBACK_URL)
finder = psq.UserFinder(authenticator)

pusher.app_id='19318'
pusher.key='890abd57f862ab2712ff'
pusher.secret='00d5dd3756b1594826f2'



def newgallery(request):
    bigdict={}
    lat=request.GET['lat']
    lon=request.GET['lon']
    for i in range(1,16):
        d=api.search(geocode=lat+','+lon+',1mi',rpp='100',page=i)
        for result in d:
            if result in bigdict:
                pass
            else:
                bigdict[result.from_user_id]=re.sub('_normal','',result.profile_image_url)
    return render_to_response('newgallery.html',{'bigdict':bigdict})
        

def oldergallery(request):
    #u=user.objects.get(fsq_id=request.session['fsq_id'])
    token = '1A0ESOQC4W2RIGY442CJTKKFJEM04BYCEHSG0SNCVIWMKPII'
    lat=request.GET['lat']
    lon=request.GET['lon']
    gender=request.GET['gender']

    trending=authenticator.query("/venues/trending", token, {'ll':str(lat)+','+str(lon)})
    trending_venues={}
    nearby_venues={}
    for item in trending['venues']:
        try:
            trending_venues[item['id']]=item['name'],item['categories'][0]['name']
        except:
            trending_venues[item['id']]=item['name'],''
    else:
        pass
    radius=2
    all_nearby = authenticator.query("/venues/search", token, {'ll':str(lat)+','+str(lon), 'limit':50, 'intent':'browse', 'radius':radius})
    i=0
    for item in all_nearby['venues']:
        if item['hereNow']['count']>0:
            try:
                nearby_venues[item['id']]=item['name'], item['categories'][0]['name']
            except:
                nearby_venues[item['id']]=item['name'],''
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
            herenow[i]['hereNow']['venueCat']=venue[1][1]
            i = i+1
    for item in herenow:
            venueName=item['hereNow']['venueName']
            venueCat=item['hereNow']['venueCat']
            for entry in item['hereNow']['items']:
                    if entry['user']['gender']==gender:
                            the_id=entry['user']['id']
                            query = finder.findUser(token, the_id)
                            twitter=query.twitter()
                            if entry['user']['photo'].startswith("https://foursquare.com/img/"):
                                    pass
                            elif not twitter:
                                    pass
                            elif categorize(venueName):
                                chickpix[the_id]=[entry['user']['photo'][36:],entry['user']['firstName'],venueName.split('-')[0],v_ids[n],twitter]
                            else:
                                backpix[the_id]=[entry['user']['photo'][36:],entry['user']['firstName'],venueName.split('-')[0],v_ids[n],twitter]
                    else:
                            pass
            n+=1
    preferred=[list(x) for x in chunk(chickpix.values(), 2)]
    other=[list(x) for x in chunk(backpix.values(), 2)]
    pairs=preferred+other
    return render_to_response('newgallery.html', {'pairs':pairs})


def ajaxreq(request):
    u=user.objects.get(fsq_id=request.session['fsq_id'])
    #token = '1A0ESOQC4W2RIGY442CJTKKFJEM04BYCEHSG0SNCVIWMKPII'
    lat=request.GET['lat']
    lon=request.GET['lon']
    gender=request.GET['gender']
    token = u.token
    HttpResponse('success')
    trending=authenticator.query("/venues/trending", token, {'ll':str(lat)+','+str(lon)})
    trending_venues={}
    nearby_venues={}
    for item in trending['venues']:
        try:
            trending_venues[item['id']]=item['name'],item['categories'][0]['name']
        except:
            trending_venues[item['id']]=item['name'],''
    else:
        pass
    radius='1000'
    all_nearby = authenticator.query("/venues/search", token, {'ll':str(lat)+','+str(lon), 'limit':50, 'intent':'browse', 'radius':radius})
    i=0
    for item in all_nearby['venues']:
        if item['hereNow']['count']>0:
            try:
                nearby_venues[item['id']]=item['name'], item['categories'][0]['name']
            except:
                nearby_venues[item['id']]=item['name'],''
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
            herenow[i]['hereNow']['venueCat']=venue[1][1]
            i = i+1
    for item in herenow:
            venueName=item['hereNow']['venueName']
            venueCat=item['hereNow']['venueCat']
            for entry in item['hereNow']['items']:
                    if entry['user']['gender']==gender:
                            the_id=entry['user']['id']
                            query = finder.findUser(token, the_id)
                            twitter=query.twitter()
                            if entry['user']['photo'].startswith("https://foursquare.com/img/"):
                                    pass
                            elif not twitter:
                                    pass
                            elif categorize(venueName):
                                chickpix[the_id]=[entry['user']['photo'][36:],entry['user']['firstName'],venueName.split('-')[0],v_ids[n],twitter]
                            else:
                                backpix[the_id]=[entry['user']['photo'][36:],entry['user']['firstName'],venueName.split('-')[0],v_ids[n],twitter]
                    else:
                            pass
            n+=1
    p = pusher.Pusher()
    p['chickpix'].trigger('done', {'chickpix': chickpix, 'backpix':backpix})
    return

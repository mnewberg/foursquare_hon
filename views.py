from django.http import HttpResponse, HttpResponseRedirect 
from django.shortcuts import render_to_response
import pysq.apiv2 as psq
from gallery.models import user, rating, record, user_lookup, invite_codes, venue_ll
from django.template import RequestContext
from django.core.context_processors import csrf
from randomizer import chunk
import os
import random
from time import time
import datetime
from leaderboard import suggested_venues
from django.template.defaultfilters import stringfilter
from haversine import *
import urllib
import urllib2
from detection import *
import re

authenticator = psq.FSAuthenticator('W1EKUBNDSX3ROZJB5HCIIDZPIHNM5FPUSEYWW03GA5WTLC0G','TN2N44EY3SQ0M43TIV2KZKDH5NKHJ4ROWM5Z5W0G1KL1UXEP','http://tryfourplay.com/loc/')

def postrecv(request):
    os.chdir("/var/www/foursquare/")
    os.system("git pull origin master")
    return HttpResponse('Vote added')

def home(request):
    user_agent = get_user_agent(request)
    if is_desktop(user_agent):
        return render_to_response('home.html')
    else:
        return render_to_response('home.html')

def login(request):
	request.session['invite_code']=request.GET['invite_code']
	request.session.set_expiry(0)
        uri = authenticator.authorize_uri()
	return HttpResponseRedirect(uri)
	

def second(request):
	request.session['code']=request.GET['code']
	authenticator.set_token(request.session['code'])
	da_id=authenticator.query("/users/self")
	f_id=da_id['user']['id']
	finder = psq.UserFinder(authenticator)
	query = finder.findUser(f_id)
        request.session['fsq_id']=f_id

        try:
            invite_code= request.session['invite_code']
        except:
            return render_to_response('wait.html') 
        

	## does user already exist in user table? IF invite set to true, render to response loc
	if user.objects.filter(fsq_id=f_id, invite=True).count()==1:
		return render_to_response('loc.html')
##RETURNING USER
        elif user.objects.filter(fsq_id=f_id, invite=False).count()==1 and invite_codes.objects.filter(code=invite_code).count()==1:
                i=invite_codes.objects.get(code=invite_code)
                i.quota-=1
                i.save()
                u=user.objects.get(fsq_id=f_id)
                u.invite=True
                u.save()
                return render_to_response('loc.html')
##correct invite code THIS Time. Last time wasn't in.
	elif invite_codes.objects.filter(code=invite_code).count()==1 and user.objects.filter(fsq_id=f_id).count()==0:
		request.session['fsq_id']=f_id
		u1 = user.objects.create(fsq_id=query.id(), first_name=query.first_name(), last_name=query.last_name(),date_joined=datetime.datetime.today(),phone=query.phone(),email=query.email(),twitter=query.twitter(),facebook=query.facebook(),photo=query.photo()[44:], has_shared=False, invite=True)
		i=invite_codes.objects.get(code=invite_code)
		i.quota-=1
		i.save()
		return render_to_response('loc.html')
## first time in, correct invite
	elif user.objects.filter(fsq_id=f_id).count()==1:
               return render_to_response('wait.html')
##not first time in, you didnt guess correctly
        else:
                u1 = user.objects.create(fsq_id=query.id(), first_name=query.first_name(), last_name=query.last_name(),date_joined=datetime.datetime.today(),phone=query.phone(),email=query.email(),twitter=query.twitter(),facebook=query.facebook(),photo=query.photo()[44:], has_shared=False, invite=False)
## first time in, didn't guess correctly		
		return render_to_response('wait.html')
    
def gallery(request, page):
	if page=='0':
		lat=request.GET['lat']
		lon=request.GET['lon']
		gender=request.GET['gender']
		request.session['gender']=gender
		request.session['lat']=lat
		request.session['lon']=lon
		params = {}
		params.update(csrf(request))
		authenticator.set_token(request.session['code'])

		trending=authenticator.query("/venues/trending", {'ll':str(lat)+','+str(lon)})
		trending_venues={}
		nearby_venues={}
		for item in trending['venues']:
		    trending_venues[item['id']]=item['name']
                radius=request.GET['radius']
		if haversine(float(lat), float(lon), 40.7587,-73.984509)<6 and radius<=10000:
                    radius=2000
                else:
                    pass
                request.session['radius']=radius
                all_nearby = authenticator.query("/venues/search", {'ll':str(lat)+','+str(lon), 'limit':50, 'intent':'browse', 'radius':radius})
                i=0
		for item in all_nearby['venues']:
		    if item['hereNow']['count']>0:
		        nearby_venues[item['id']]=item['name']
		for item in set(nearby_venues).intersection(set(trending_venues)):
			del nearby_venues[item]
		all_venues_nearby = nearby_venues.items() + trending_venues.items()	
		venue_names=[]
		chickpix={}
		herenow=[]
		v_ids=[]
		i=0
		n=0
		for venue in all_venues_nearby:
			herenow.append(authenticator.query("/venues/"+venue[0]+"/herenow"))
			v_ids.append(venue[0])
			herenow[i]['hereNow']['venueName']=venue[1]
			i = i+1
	    	for item in herenow:
			venueName=item['hereNow']['venueName']
			for entry in item['hereNow']['items']:
				if entry['user']['gender']==gender:
					the_id=entry['user']['id']
					if entry['user']['photo'].startswith("https://foursquare.com/img/"):
						pass
					else:
						chickpix[the_id]=[entry['user']['photo'][44:],entry['user']['firstName'],venueName,v_ids[n]]
                                                try: 
                                                    user_lookup.objects.create(fsq_id=entry['user']['id'],pic_id=entry['user']['photo'][44:])
                                                except:
                                                    pass
                                else:
					pass
			n+=1
		
		pairs=[list(x) for x in chunk(chickpix.values(), 2)]
		for item in pairs:
			if len(item)<2:
				item.append(pairs[0][0])
		random.shuffle(pairs)
		request.session['chickpix']=pairs
        else:
		params = {}
		params.update(csrf(request))
        request.session.modified = True
        if len(request.session['chickpix'])<(int(page)+1):
            newradius=int(request.session['radius'])+15000
            request.session['radius']=newradius
            if newradius>100000:
                lastpage=True
            else:
                lastpage=False
            return render_to_response('lastpage.html', {'newradius':newradius,'lastpage':lastpage, 'gender':request.session['gender'], 'lat':request.session['lat'], 'lon':request.session['lon']})
        else:
            image_pair=request.session['chickpix'][int(page)]
            return render_to_response ('gallery.html', {'chickpix':image_pair, 'csrf':params, 'page':int(page)}, context_instance=RequestContext(request))
    
def vote(request):
	authenticator.set_token(request.session['code'])
	pic_id = request.POST['chosen_id']
	pic_id2 = request.POST['pic_id2']
	venue_id=request.POST['venue_id']
   	venue_id2=request.POST['venue_id2']
	thetime=round(time())
	
	if rating.objects.filter(pic_id=pic_id).count()==1:
		r1 = rating.objects.get(pic_id=pic_id)
		r1.rating += 1
		r1.total_sets += 1
	else:
		r1 = rating(pic_id=pic_id, rating=1, total_sets=1)
	r1.save()
	record1=record.objects.create(time=thetime, venue_id=venue_id, target=r1)
	if rating.objects.filter(pic_id=pic_id2).count()==1:
		r2 = rating.objects.get(pic_id=pic_id2)
		r2.total_sets +=1
	else:        
		r2 = rating(pic_id=pic_id2, rating=0, total_sets=1)
	r2.save()
	record2=record.objects.create(time=thetime, venue_id=venue_id2, target=r2)
	fsq_user = user.objects.get(fsq_id=request.session['fsq_id'])
	fsq_user.records.add(record1)
	fsq_user.save()
	for place in venue_id, venue_id2:
            try: 
                location=authenticator.query("/venues/"+place)
                venue_ll.objects.create(venue_id=place, lat=float(location['venue']['location']['lat']), lon=float(location['venue']['location']['lng']))
            except:
                pass

	return HttpResponse('Vote successful')

def results(request):
	authenticator.set_token(request.session['code'])
	fsq_id=request.session['fsq_id']
        u=user.objects.get(fsq_id=fsq_id)
	## if u.has_shared==False:
            ## post_data=[('oauth_token',authenticator.auth_param()[13:]),('shout','I\'m checking out people nearby on Fourplay.com! This is nuts.'),('broadcast','public,followers')]
            ## urllib2.urlopen('https://api.foursquare.com/v2/checkins/add',urllib.urlencode(post_data))
            ## u.has_shared=True
            ## u.save()
        da_results=suggested_venues(fsq_id)
	venue_names={}
	for item in da_results:
		data=authenticator.query("/venues/"+item[0])
		try:
                    venue_names[data['venue']['name']]=[data['venue']['location']['address'], data['venue']['location']['postalCode'], item[1],re.sub(' ','+',data['venue']['location']['address'])]
                except:
                    pass
                global_results=suggested_venues('',request.session['lat'],request.session['lon'],request.session['radius'])
	all_venues={}
	for item in global_results:
		data=authenticator.query("/venues/"+item[0])
                try:
                    all_venues[data['venue']['name']]=[data['venue']['location']['address'], data['venue']['location']['postalCode'], item[1],re.sub(' ','+',data['venue']['location']['address'])]
                except:
                    pass
	return render_to_response('results.html', {'your_venue_names':venue_names, 'all_venues':all_venues})

def dialog(request, image):
    return render_to_response('popup.html',{'image':image})

def notice(request):
    return render_to_response('warning.html')

def faq(request):
    return render_to_response('faq.html')

def tos(request):
    return render_to_response('tos.html')

def checkin(request):
        authenticator.set_token(request.session['code'])
        fsq_id=request.session['fsq_id']
        u=user.objects.get(fsq_id=fsq_id)
        post_data=[('oauth_token',authenticator.auth_param()[13:]),('shout','I\'m having a blast on Fourplay! TryFourplay.com'),('broadcast','public,followers')]
        urllib2.urlopen('https://api.foursquare.com/v2/checkins/add',urllib.urlencode(post_data))
        u.has_shared=True
        u.save()
        return HttpResponseRedirect('http://tryfourplay.com')

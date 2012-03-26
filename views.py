from django.http import HttpResponse, HttpResponseRedirect 
from django.shortcuts import render_to_response
import pysq.apiv2 as psq
from gallery.models import user, rating, record, user_lookup, venue_ll, twitter_outreach
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
from categorize import *
import settings
from id_gen import random_string
from shout_twitter import send_twitter_shout, get_bio
from sms.text import *
from django.utils import simplejson

authenticator = psq.FSAuthenticator(settings.CLIENT_ID, settings.CLIENT_SECRET, settings.CALLBACK_URL)

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
        uri = authenticator.authorize_uri()
	return HttpResponseRedirect(uri)

def scrub(name):
    try:
        return re.sub('\&#.*;',' ',name)
    except:
        pass

def second(request):
	token=authenticator.set_token(request.GET['code'])
      	da_id=authenticator.query("/users/self", token, None)
	f_id=da_id['user']['id']
	finder = psq.UserFinder(authenticator)
	query = finder.findUser(token, f_id)
	request.session['fsq_id']=f_id
        request.session.set_expiry(0)
        last_name=query.last_name()
        showmessage=True
        try:
            user_look=user_lookup.objects.get(fsq_id=f_id)
            unread=twitter_outreach.objects.filter(m_target=user_look, read=False).count()
        except:
            showmessage=False
            unread=False 
        try:
            last_name=scrub(last_name)
        except:
            pass
        try:
            user_look=user_lookup.objects.get(fsq_id=f_id)
        except:
            user_look=False
        if showmessage==False and user_look!=False:
                u=user.objects.get(fsq_id=f_id)
                u.token=token
                u.photo=query.photo()[37:]
                has_shared=u.has_shared
                u.save()
                return render_to_response('loc.html', {'has_shared':has_shared})
        elif unread and twitter_outreach.objects.get(uid=request.session['uid']).m_target.fsq_id != f_id:
                return HttpResponse ('INVALID LOGIN ATTEMPT')
	elif unread>0 and user.objects.filter(fsq_id=f_id).count()==0:
		user.objects.create(fsq_id=query.id(), first_name=scrub(query.first_name()), last_name=last_name,date_joined=datetime.datetime.today(),phone=query.phone(),email=query.email(),twitter=query.twitter(),facebook=query.facebook(),photo=query.photo()[37:], has_shared=False, token=token)
                if not query.phone():
                    return render_to_response('missing.html')
                else:
                    return HttpResponseRedirect('/callback')
	elif unread>0:
                if not user.objects.get(fsq_id=f_id).phone:
                    return render_to_response('missing.html')
		else:
                    return HttpResponseRedirect('/callback')
	elif user.objects.filter(fsq_id=f_id).count()==1:
		u=user.objects.get(fsq_id=f_id)
		u.token=token
                u.photo=query.photo()[36:]
                has_shared=u.has_shared
		u.save()
		return render_to_response('loc.html', {'has_shared':has_shared})
##RETURNING USER
	else:
		request.session['fsq_id']=f_id
		user.objects.create(fsq_id=query.id(), first_name=scrub(query.first_name()), last_name=scrub(query.last_name()),date_joined=datetime.datetime.today(),phone=query.phone(),email=query.email(),twitter=query.twitter(),facebook=query.facebook(),photo=query.photo()[36:], has_shared=False, token=token)
		return render_to_response('loc.html')

    
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
		u=user.objects.get(fsq_id=request.session['fsq_id'])
		token = u.token
		u.last_lat=lat
		u.last_lon=lon
		u.save()
		trending=authenticator.query("/venues/trending", token, {'ll':str(lat)+','+str(lon)})
		trending_venues={}
		nearby_venues={}
		for item in trending['venues']:
		    try:
                        trending_venues[item['id']]=item['name'],item['categories'][0]['name']
                    except:
                        trending_venues[item['id']]=item['name'],''
                radius=request.GET['radius']
		if haversine(float(lat), float(lon), 40.7587,-73.984509)<6 and radius<=10000:
                    radius=2000
                else:
                    pass
                request.session['radius']=radius
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
                if len(all_venues_nearby)<16:
                    return render_to_response ('block.html')
                else:
                    pass
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
					if entry['user']['photo'].startswith("https://foursquare.com/img/"):
						pass
					elif categorize(venueName):
                                            chickpix[the_id]=[entry['user']['photo'][36:],entry['user']['firstName'],venueName.split('-')[0],v_ids[n]]
                                        else:
                                            backpix[the_id]=[entry['user']['photo'][36:],entry['user']['firstName'],venueName.split('-')[0],v_ids[n]]
                                        
                                        try: 
                                            user_lookup.objects.create(fsq_id=entry['user']['id'],pic_id=entry['user']['photo'][36:])
                                        except:
                                            pass
                                        
                                else:
					pass
			n+=1
		
		preferred=[list(x) for x in chunk(chickpix.values(), 2)]
		other=[list(x) for x in chunk(backpix.values(), 2)]
                random.shuffle(preferred)
                random.shuffle(other)
                pairs=preferred+other
                for item in pairs:
			if len(item)<2:
				item.append(pairs[0][0])
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

def has_twitter(request):
    pic_id=request.GET['pic_id']
    the_id=user_lookup.objects.get(pic_id=pic_id).fsq_id
    token = user.objects.get(fsq_id=request.session['fsq_id']).token
    finder = psq.UserFinder(authenticator)
    query = finder.findUser(token, the_id)
    if query.twitter():
        twitter=True
    else:
        twitter=False
    return HttpResponse(simplejson.dumps({'twitter':twitter}), mimetype='application/javascript')

def vote(request):
        token = user.objects.get(fsq_id=request.session['fsq_id']).token
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
                location=authenticator.query("/venues/"+place,token)
                venue_ll.objects.create(venue_id=place, lat=float(location['venue']['location']['lat']), lon=float(location['venue']['location']['lng']))
            except:
                pass

	return HttpResponse('Vote successful')

def results(request):
        
	fsq_id=request.session['fsq_id']
	u=user.objects.get(fsq_id=fsq_id)
	token = u.token

	if u.has_shared==False:
            post_data=[('oauth_token',token),('shout','I\'m checking out people nearby on TryFourplay.com! This is nuts.'),('broadcast','public,followers')]
            urllib2.urlopen('https://api.foursquare.com/v2/checkins/add',urllib.urlencode(post_data))
            u.has_shared=True
            u.save()
        da_results=suggested_venues(fsq_id)
	
        venue_names={}
        
	for item in da_results:
		data=authenticator.query("venues/"+item[0],token)
		try:
                    venue_names[data['venue']['name']]=[data['venue']['location']['address'], data['venue']['location']['postalCode'], item[1][0],re.sub(' ','+',data['venue']['location']['address']),item[1][1]]
                except:
                    pass
        global_results=suggested_venues('',request.session['lat'],request.session['lon'],request.session['radius'])
	all_venues={}
	for item in global_results:
		data=authenticator.query("venues/"+item[0],token)
                try:
                    all_venues[data['venue']['name']]=[data['venue']['location']['address'], data['venue']['location']['postalCode'], item[1][0],re.sub(' ','+',data['venue']['location']['address']),item[1][1]]
                except:
                    pass
	return render_to_response('results.html', {'your_venue_names':venue_names, 'all_venues':all_venues})

def dialog(request, image):
    venue=request.GET['venue_id']
    token = user.objects.get(fsq_id=request.session['fsq_id']).token
    t=user_lookup.objects.get(pic_id=image)
    the_id=t.fsq_id
    finder = psq.UserFinder(authenticator)
    query = finder.findUser(token, the_id)
    twitter=query.twitter()
    if twitter:
        has_twitter=True
        t.t_handle=twitter
        t.save()
        request.session['venue']=venue
        request.session['f_name']=query.first_name()
        request.session['t_handle']=twitter
        request.session['t_pic']=image
    else:
        has_twitter=False

    return render_to_response('popup.html',{'image':image, 'twitter':has_twitter, 'f_name':query.first_name()})

def pickmessage(request):
    fsq_id=request.session['fsq_id']
    the_user=user.objects.get(fsq_id=fsq_id)
    if len(the_user.photo)<=4:
        return render_to_response('error_photo.html')
    else:
        pass
    params={}
    params.update(csrf(request))
    if request.GET['from_hon_screen']=='true':
        venue=request.GET['venue_id']
        image=request.GET['pic_id']
        t=user_lookup.objects.get(pic_id=image)
        token = the_user.token
        the_id=t.fsq_id
        finder = psq.UserFinder(authenticator)
        query = finder.findUser(token, the_id)
        twitter=query.twitter()
        target_t=twitter
        target_p=image
        target_n=query.first_name()
        target_v=venue
    else:
        target_t=request.session['t_handle']
        target_p=request.session['t_pic']
        target_n=request.session['f_name']
        target_v=request.session['venue']

    return render_to_response('message.html', {'t_handle':target_t,'t_pic':target_p,'f_name':target_n, 'venue_id':target_v, 'csrf':params}, context_instance=RequestContext(request))

def outreach(request):
    params = {}
    params.update(csrf(request))

    message=request.POST['message']
    t_handle=request.POST['t_handle']
    venue=request.POST['venue_id']
    f_name=request.POST['f_name']
    v=authenticator.userless_query("/venues/"+venue)
    venue_name=v['venue']['name']
    uid=random_string(5)
    datarget=user_lookup.objects.get(pic_id=request.POST['t_pic'])
    sender=user.objects.get(fsq_id=request.session['fsq_id'])
    twitter_outreach.objects.create(m_target=datarget, sender=sender, uid=uid, message=message, read=False, venue_id=venue)
    tweet_response = send_twitter_shout(t_handle,sender.first_name,f_name,venue_name,uid)
    if tweet_response and sender.phone:
        return render_to_response('sent.html')
    elif not sender.phone:
        return render_to_response('missing_sender.html', {'csrf':params}, context_instance=RequestContext(request))
    else:
        return render_to_response('error.html')

def onboard(request, uid):
    t=twitter_outreach.objects.get(uid=uid)
    sender=t.sender
    the_user=user.objects.get(fsq_id=sender)
    msg=t.message
    venue=t.venue_id
    
    try:
        location,bio=get_bio(the_user.twitter)
    except:
        location,bio='',''
    v=authenticator.userless_query("/venues/"+venue)
    vlat=v['venue']['location']['lat']
    vlon=v['venue']['location']['lng']
    venue_name=v['venue']['name']
    
    request.session['uid']=uid
    request.session.set_expiry(0)
    return render_to_response('onboard.html',{'pic':the_user.photo,'first_name':the_user.first_name,'twitter':the_user.twitter, 'message':msg, 'venue':venue_name, 'location':location, 'bio':bio})

def notice(request):
    return render_to_response('warning.html')

def faq(request):
    return render_to_response('faq.html')

def tos(request):
    return render_to_response('tos.html')

def checkin(request):        
        token = user.objects.get(fsq_id=request.session['fsq_id']).token
        post_data=[('oauth_token',token),('CHECKIN_ID','4f451ed2e4b0f1d45d9062da'),('text','Does this work?')]
        urllib2.urlopen('https://api.foursquare.com/v2/checkins/4f451ed2e4b0f1d45d9062da/addcomment',urllib.urlencode(post_data))
        
        return HttpResponseRedirect('http://tryfourplay.com')

def missing(request):
    params = {}
    params.update(csrf(request))

    error=False
    phone=request.POST['area_code']+request.POST['number1']+request.POST['number2']
    try:
        source=request.POST['user']
    except:
        source='recipient'
    
    if len(re.sub('[^\d.]+','',phone))!=10:
        if source=='sender':
            return render_to_response('missing_sender.html',{'error':True, 'csrf':params}, context_instance=RequestContext(request))
        else:
            return render_to_response('missing.html',{'error':True})
    else:
        pass
    u=user.objects.get(fsq_id=request.session['fsq_id'])
    u.phone=re.sub('[^\d.]+','',phone)
    u.save()
    if source=='sender':
        return render_to_response('sent.html')
    else:
        return HttpResponseRedirect('/login')

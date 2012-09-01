from sendemail import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
import pysq.apiv2 as psq
from gallery.models import user, rating, record, user_lookup, venue_ll, twitter_outreach, invite_codes, game, queue
from django.template import RequestContext
from django.core.context_processors import csrf
import os
import random
from time import time
import datetime
from leaderboard import suggested_venues
from django.template.defaultfilters import stringfilter
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
from pyklout import Klout
import subprocess
from django.views.decorators.csrf import csrf_exempt
import json
import time
import tweepy
import logging 

authenticator = psq.FSAuthenticator(settings.CLIENT_ID, settings.CLIENT_SECRET, settings.CALLBACK_URL)
consumer_key=settings.CONSUMER_KEY
consumer_secret=settings.CONSUMER_SECRET
access_token=settings.ACCESS_TOKEN
access_token_secret=settings.ACCESS_TOKEN_SECRET
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

logger=logging.getLogger('django.request')


def postrecv(request):
    subprocess.call(['/var/www/four_staging/foursquare/pull.sh'])
    print 'pull'
    return HttpResponse('pull')

def home(request):
    user_agent = get_user_agent(request)
    if is_desktop(user_agent):
        return render_to_response('desktop.html')
    else:
        return render_to_response('front_2.html')

def login(request):
        try:
            request.session['lat']=request.GET['lat']
            request.session['lon']=request.GET['lon']
        except:
			if 'fsqCallback' in request.GET:
				dastring=request.GET['fsqCallback']
                                cid=dastring[22:46]
                                request.session['callback']=cid
				d=authenticator.query("/checkins/"+cid,'1A0ESOQC4W2RIGY442CJTKKFJEM04BYCEHSG0SNCVIWMKPII')
                                f_id=d['checkin']['user']['id']
                                request.session['fsq_id']=f_id
                                request.session['lat']=d['checkin']['venue']['location']['lat']
                                request.session['lon']=d['checkin']['venue']['location']['lng']

                                return HttpResponseRedirect('/loc')
			else:
				print 'problem'
        uri = authenticator.authorize_uri()
        try:
            request.session['invite_code']=request.GET['invite_code']
        except:
            pass
	return HttpResponseRedirect(uri)

def scrub(name):
    try:
        return re.sub('\\\\U\w*',' ',name)
    except:
        pass

def second(request):
      try:
          lat=request.session['lat']
          lon=request.session['lon']
      except:
          lat=0
          lon=0
      params = {}
      params.update(csrf(request))
      #user coming from foursquare.app
      if 'callback' in request.session:
          f_id=request.session['fsq_id']
          u=user.objects.get(fsq_id=f_id)
          return render_to_response('loc.html', {'from_4app':True,'sex':u.gender, 'twitter':u.twitter,'token':u.token,'csrf':params,'lat':lat,'lon':lon,'phone':u.phone}, context_instance=RequestContext(request))
      else:
          pass
      try:
            invite_code=request.session['invite_code']
      except:
            invite_code=''
      token=authenticator.set_token(request.GET['code'])
      da_id=authenticator.query("/users/self", token, None)
      f_id=da_id['user']['id']
        ## onboarded user wants to unsubscribe, reroute flow
      if 'unsubscribe' in request.session:
            u=user_lookup.objects.get(fsq_id=f_id)
            try:
                t=twitter_outreach.objects.get(m_target=u)
                if t.m_target.fsq_id==f_id:
                    u.unsubscribed=True
                    u.save()
                    return HttpResponse("Unsubscribe successful")
                else:
                    pass
            except:
                 pass
      else:
            pass
        ## onboarded user wants to block particular user, reroute flow
      if 'block' in request.session:
            uid=request.session['uid']
            try:
                t=twitter_outreach.objects.get(uid=uid)
                if t.m_target.fsq_id==f_id:
                    u=user_lookup.objects.get(fsq_id=t.m_target.fsq_id)
                    u.blocks.add(user.objects.get(fsq_id=t.sender.fsq_id))
                    u.save()
                    return HttpResponse("You will no longer receive messages from this user")
                else:
                    pass
            except:
                pass
      else:
            pass
      finder = psq.UserFinder(authenticator)
      query = finder.findUser(token, f_id)
      request.session['fsq_id']=f_id
      request.session.set_expiry(0)
      last_name=query.last_name()
      showmessage=True
      params = {}
      params.update(csrf(request))
      try:
          if time.time()-query.data['checkins']['items'][0]['createdAt'] < 3600:
              recentcheckin=True
          else:
              recentcheckin=False
      except:
          recentcheckin=False
      if 'uid' in request.session:
            uidsesh=True
      else:
            uidsesh=False
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
      if showmessage==False and user_look!=False and invite_codes.objects.filter(code=invite_code).count()==1:
                u=user.objects.get(fsq_id=f_id)
                u.token=token
                u.photo=query.photo()[36:]
                u.last_lat=lat
                u.last_lon=lon
                has_shared=u.has_shared
                u.save()
                return render_to_response('loc.html', {'lat':lat,'lon':lon,'sex':query.gender(),'token':token, 'twitter':u.twitter(),'recentcheckin':recentcheckin,'phone':u.phone, 'has_shared':has_shared,'token':token,'csrf':params}, context_instance=RequestContext(request))
      elif unread and uidsesh and twitter_outreach.objects.get(uid=request.session['uid']).m_target.fsq_id != f_id:
                return HttpResponse ('INVALID LOGIN ATTEMPT')
      elif unread>0 and uidsesh and user.objects.filter(fsq_id=f_id).count()==0:
		sobjects.create(fsq_id=query.id(), first_name=scrub(query.first_name()), last_name=last_name,date_joined=datetime.datetime.today(),phone=query.phone(),email=query.email(),twitter=query.twitter(),facebook=query.facebook(),photo=query.photo()[36:], has_shared=False, token=token, gender=query.gender())
                if not query.phone():
                    return render_to_response('missing.html',{'role':'onboard'}, context_instance=RequestContext(request))
                else:
                    return HttpResponseRedirect('/callback')
      elif unread>0:
                if not user.objects.get(fsq_id=f_id).phone:
                    return render_to_response('missing.html',{'role':'onboard'}, context_instance=RequestContext(request))
		else:
                    return HttpResponseRedirect('/callback')
      elif user.objects.filter(fsq_id=f_id).count()==1:
		u=user.objects.get(fsq_id=f_id)
		u.token=token
                try:
                    u.last_lat=lat
                    u.last_lon=lon
                except:
                    pass
                u.photo=query.photo()[36:]
                has_shared=u.has_shared
		u.save()
		return render_to_response('loc.html', {'lat':lat,'lon':lon,'has_shared':has_shared,'sex':query.gender(),'token':token, 'twitter':u.twitter,'phone':u.phone,'recentcheckin':recentcheckin,'csrf':params}, context_instance=RequestContext(request))
##RETURNING USER
      elif invite_codes.objects.filter(code=invite_code).count()==1:
		request.session['fsq_id']=f_id
		u=user.objects.create(fsq_id=query.id(), first_name=scrub(query.first_name()), last_name=scrub(query.last_name()),date_joined=datetime.datetime.today(),phone=query.phone(),email=query.email(),twitter=query.twitter(),facebook=query.facebook(),photo=query.photo()[36:], has_shared=False, token=token, gender=query.gender())
                welcome_email(u.email(),u.first_name())
                authenticator.query("/users/6478/request",u.token,None)
                invite_codes.objects.get(code=invite_code).delete()
                return render_to_response('loc.html', {'lat':lat,'lon':lon,'sex':query.gender(),'token':token,'phone':query.phone(), 'twitter':query.twitter(),'recentcheckin':recentcheckin,'csrf':params}, context_instance=RequestContext(request))
      elif queue.objects.filter(fsq_id=query.id()).count()==0:
                the_code=invite_codes.objects.create(code=random_string(7),quota=1)
                queue.objects.create(fsq_id=query.id(),first_name=scrub(query.first_name()),last_name=scrub(query.last_name()),date_joined=datetime.datetime.today(),token=token,email=query.email(),allocated_invite=the_code, lat=request.session['lat'],lon=request.session['lon'])
                if len(re.findall('blank',query.photo()))>0:
                    photo=False
                else:
                    photo=True
                queue_email(query.email(),query.first_name())
                return render_to_response('thank_you.html',{'photo':photo})
      else:
                logger.error('Login exception', exc_info=True, extra={'stack': True})
                return render_to_response('thank_you.html')
    



def pickmessage(request):
    api=Klout(settings.KLOUT)
    t_api = tweepy.API(auth)
    fsq_id=request.session['fsq_id']
    the_user=user.objects.get(fsq_id=fsq_id)
    params={}
    params.update(csrf(request))
    
    venue=request.GET['venue_id']
    image=request.GET['pic_id']
    try:
        r=rating.objects.get(pic_id=image)
        r.rating+=1
        r.save()
    except:
        r=rating.objects.create(pic_id=image,rating=1)
    u=user.objects.get(fsq_id=fsq_id)
    rec=record.objects.create(target=r,time=int(time.time()))
    u.records.add(rec)
    
    t=user_lookup.objects.get(pic_id=image)
    target_t=t.t_handle
    target_n=t.first_name
    target_v=venue
    t_bio=t_api.get_user(screen_name=target_t).description
    try:
        the_id=api.identity(str(target_t),'twitter')['id']
        topics=api.topics(the_id)
        tlist=[]
    except:
        topics=[]
        tlist=[]
        
    for i in topics:
        tlist.append(i['displayName'])
    
    games=game.objects.all()
    #    target_t=request.session['t_handle']
     #   target_p=request.session['t_pic']
      #  target_n=request.session['f_name']
       # target_v=request.session['venue']
    
    return render_to_response('pick_a_game.html', {'t_handle':target_t,'t_pic':image,'f_name':target_n, 'venue_id':target_v, 'csrf':params,'topics':tlist,'games':games,'t_bio':t_bio}, context_instance=RequestContext(request))

def outreach(request):
    params = {}
    params.update(csrf(request))
    
    game_id=request.POST['game_id']
    t_handle=request.POST['t_handle']
    venue=request.POST['venue_id']
    f_name=request.POST['f_name']
    v=authenticator.userless_query("/venues/"+venue)
    venue_name=v['venue']['name']
    uid=random_string(5)
    
    thegame=game.objects.get(gid=game_id)
    message='N/A'

    datarget=user_lookup.objects.get(pic_id=request.POST['t_pic'])
    sender=user.objects.get(fsq_id=request.session['fsq_id'])
    if datarget.unsubscribed==True or sender in datarget.blocks.all():
        return HttpResponse(simplejson.dumps({'error':True,'optout':True}),mimetype='application/json')
    else:
        pass
    twitter_outreach.objects.create(m_target=datarget, sender=sender,game=thegame, uid=uid, message=message, read=False, venue_id=venue)
    tweet_response = send_twitter_shout(t_handle,sender.first_name,f_name,venue_name,uid)
    if tweet_response:
        return HttpResponse(simplejson.dumps({'error':False}), mimetype='application/json')
    else:
        logger.error('There was a twitter error', exc_info=True, extra={'stack': True})
        return HttpResponse(simplejson.dumps({'error':True,'optout':False}),mimetype='application/json')

def onboard(request, uid):
    user_agent = get_user_agent(request)
    if is_desktop(user_agent):
        return render_to_response('desktop.html')
    else:
        pass
    t=twitter_outreach.objects.get(uid=uid)
    sender=t.sender
    the_user=user.objects.get(fsq_id=sender)
    msg=t.message
    venue=t.venue_id
    try:
        location,bio=get_bio(the_user.twitter)
    except:
        location,bio='',''
    v=authenticator.userless_query("venues/"+venue)
    venue_name=v['venue']['name']
    
    v2=authenticator.query("/users/self",the_user.token, None)
    last_checkin=v2['user']['checkins']['items'][0]['venue']['name']
    last_checkin_id=v2['user']['checkins']['items'][0]['venue']['id']
    t.other_venue_id=last_checkin_id
    t.save()
    request.session['uid']=uid
    request.session.set_expiry(120)
    return render_to_response('on_board.html',{'pic':the_user.photo,'first_name':the_user.first_name,'twitter':the_user.twitter, 'message':msg, 'venue':venue_name, 'location':location, 'bio':bio, 'last_checkin':last_checkin})

def notice(request):
    return render_to_response('warning.html')

def faq(request):
    return render_to_response('faq.html')

def tos(request):
    return render_to_response('tos.html')

def checkin(request):
        fsq_id=request.session['fsq_id']
        u=queue.objects.get(fsq_id=fsq_id)
        token = u.token
        post_data=[('oauth_token',token),('venueId','4fe5e2897b0c9089d7f57194'),('shout','YOU MAKE ME WANNA SHOUT! (teest)'),('broadcast','public,followers')]
        urllib2.urlopen('https://api.foursquare.com/v2/checkins/add',urllib.urlencode(post_data))
        u.has_shared=True
        u.save()
        return HttpResponseRedirect('http://playdo.pe')


def missing_sender(request):
    phone=request.POST['phone']
    u=user.objects.get(fsq_id=request.session['fsq_id'])
    u.phone=phone
    u.save()
    return HttpResponse('ok')

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
            return render_to_response('missing.html',{'error':True, 'csrf':params}, context_instance=RequestContext(request))
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
        return HttpResponseRedirect('/callback')

def unsubscribe(request):
    request.session['unsubscribe']=True
    request.session.set_expiry(120)
    uri = authenticator.authorize_uri()
    return HttpResponseRedirect(uri)

def block(request):
    uid=request.session['uid']
    request.session['block']=True
    request.session.set_expiry(120)
    t=twitter_outreach.objects.get(uid=uid)
    u=user_lookup.objects.get(fsq_id=t.m_target.fsq_id)
    u.blocks.add(user.objects.get(fsq_id=t.sender.fsq_id))
    u.save()
    uri = authenticator.authorize_uri()
    return HttpResponseRedirect(uri)


def updatetwitter(request):
    fsq_id=request.session['fsq_id']
    u=user.objects.get(fsq_id=fsq_id)
    t=request.POST['twitter']
    u.twitter=t
    u.save()
    return HttpResponse('success')

@csrf_exempt
def hook(request):
    s=request.POST["secret"]
    data=request.POST["checkin"]
    dic=json.loads(data)
    try:
        u=user.objects.get(fsq_id=dic['user']['id'])
        post_data=[('oauth_token',str(u.token)),('text','Play a game with nearby people! Click here...'),('url','http://playdo.pe/login')]
        urllib2.urlopen(str('https://api.foursquare.com/v2/checkins/'+dic['id']+'/reply'),urllib.urlencode(post_data))
    except:
        pass
    return HttpResponse('OK')

def recentcheckin(request):
	the_id=request.session['fsq_id']
	u=user.objects.get(fsq_id=the_id)
	finder=finder = psq.UserFinder(authenticator)
	query=finder.findUser(u.token,the_id)
	if time.time()-query.data['checkins']['items'][0]['createdAt'] < 3600:
		status=True
	else:
		status=False
	return HttpResponse(simplejson.dumps({'recent':status}), mimetype='application/json')



def handler500(request):
    """
    An error handler which exposes the request object to the error template.
    """
    from django.template import Context, loader
    from django.http import HttpResponseServerError
    from disqus.context_processors import default
    import logging
    import sys
    try:
        context = default(request)
    except Exception, e:
        logging.error(e, exc_info=sys.exc_info(), extra={'request': request})
        context = {}
    
    context['request'] = request
    
    t = loader.get_template('500.html') # You need to create a 500.html template.
    return HttpResponseServerError(t.render(Context(context)))

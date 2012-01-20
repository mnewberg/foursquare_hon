from django.http import HttpResponse, HttpResponseRedirect 
from django.shortcuts import render_to_response
import pysq.apiv2 as psq
from gallery.models import user, rating, record
from django.template import RequestContext
from django.core.context_processors import csrf
from randomizer import chunk
import os
import random
from time import time
import datetime


f = open('/tmp/workfile', 'w')
f.write(psq.__file__)
f.close()

authenticator = psq.FSAuthenticator('H0P2PQASLI5GNXUQSR5KN2MH4Z002YS0VSYNDFS215XNHCY5','HBDVHGLMFXFUT5SXEKLFFGBAYBXJZLGBLQ5BS232F0NGDNRG','http://4sq.getpostd.com/loc/')

# def first(request):
#     HttpResponseRedirect (uri)

def postrecv(request):
    os.chdir("/var/www/foursquare/")
    os.system("git pull origin master")
    return HttpResponse('IT WORKS')

def second(request):
     request.session['code']=request.GET['code']
     return render_to_response('loc.html')
    
def gallery(request):
	lat=request.GET['lat']
	lon=request.GET['lon']
	gender=request.GET['gender']
	params = {}
	params.update(csrf(request))
	authenticator.set_token(request.session['code'])
	if 'fsq_id' not in request.session:
		da_id=authenticator.query("/users/self")
		u1 = user.objects.create(fsq_id=da_id['user']['id'], phone=da_id['user']['contact']['phone'],
		email=da_id['user']['contact']['email'],twitter=da_id['user']['contact']['twitter'],
		facebook=da_id['user']['contact']['facebook'],photo=da_id['user']['photo'][44:], first_name=da_id['user']['firstName'], last_name=da_id['user']['lastName'],date_joined=datetime.datetime.today())
		request.session['fsq_id']=da_id['user']['id']
	else:
		pass
	trending=authenticator.query("/venues/trending", {'ll':str(lat)+','+str(lon)})
	trending_venues={}
	nearby_venues={}
	for item in trending['venues']:
	    trending_venues[item['id']]=item['name']
	all_nearby = authenticator.query("/venues/search", {'ll':str(lat)+','+str(lon)})
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
	i=0
	for venue in all_venues_nearby:
		herenow.append(authenticator.query("/venues/"+venue[0]+"/herenow"))
		herenow[i]['hereNow']['venueName']=venue[1]
		i = i+1
    	for venue in herenow:
		venueName=venue['hereNow']['venueName']
		for entry in venue['hereNow']['items']:
			if entry['user']['gender']==gender:
				the_id=entry['user']['id']
				if entry['user']['photo'][44:]=='':
					pass
				else:
					chickpix[the_id]=[entry['user']['photo'][44:],entry['user']['firstName'],venueName,entry['id']]
			else:
				pass
	rand_chickpix={}
	keys=chickpix.keys()
	random.shuffle(keys)
	for dakey in keys:
	    rand_chickpix[dakey]=chickpix[dakey]
	pairs=[list(x) for x in chunk(rand_chickpix.values(), 4)]
	if len(pairs) % 2 == 1:
	    pairs.append(pairs[0][0])
	return render_to_response ('gallery.html', {'chickpix':pairs, 'csrf':params}, context_instance=RequestContext(request))
    
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
	record1=record(time=thetime, venue_id=venue_id, target=r1)
	record1.save()
	if rating.objects.filter(pic_id=pic_id2).count()==1:
		r2 = rating.objects.get(pic_id=pic_id2)
		r2.total_sets +=1
	else:        
		r2 = rating(pic_id=pic_id2, rating=0, total_sets=1)
	r2.save()
	record2=record(time=thetime, venue_id=venue_id, target=r2)
	record2.save()
	fsq_user = user.objects.get(fsq_id=request.session['fsq_id'])
	fsq_user.ratings.add(record1, record2)
	fsq_user.save()
	
	return HttpResponse('Vote successful')
    
    
    
 
    

from django.http import HttpResponse, HttpResponseRedirect 
from django.shortcuts import render_to_response
import pysq.apiv2 as psq
from gallery.models import user, rating
from django.template import RequestContext
from django.core.context_processors import csrf
from randomizer import chunk
import os


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
		u1 = user.objects.create(fsq_id=da_id['user']['id'], phone=da_id['user']['contact']['phone'],email=da_id['user']['contact']['email'],twitter=da_id['user']['contact']['twitter'],facebook=da_id['user']['contact']['facebook'], photo=da_id['user']['photo'][44:])
		request.session['fsq_id']=da_id['user']['id']
	else:
		pass
	trending=authenticator.query("/venues/trending", {'ll':str(lat)+','+str(lon)})
	trending_venues=[]
	nearby_venues=[]
	for item in trending['venues']:
	    trending_venues.append(item['id'])
	all_nearby = authenticator.query("/venues/search", {'ll':str(lat)+','+str(lon)})
	i=0
	for item in all_nearby['venues']:
	    nearby_venues.append(item['id'])
    ## do some sort of intersection here?
	all_venues_nearby = nearby_venues + trending_venues
	for item in set(nearby_venues).intersection(set(trending_venues)):
		all_venues_nearby.remove(item)
	venue_names=[]
	for item in all_venues_nearby:
		da_venue=authenticator.query("/venues/"+item)
		venue_names.append(da_venue['venue']['name'])
	chickpix={}
	herenow=[]
	i=0
	for venue in all_venues_nearby:
		herenow.append(authenticator.query("/venues/"+venue+"/herenow"))
		herenow[i]['hereNow']['venueName']=venue_names[i]
		i = i+1
    # for item in all_nearby['venues']:
    #     if item['id'] not in herenow:
    #         venue=item['id']
    #         herenow.append(authenticator.query("/venues/"+venue+"/herenow"))
    #           herenow[i]['hereNow']['venueName']=trending['venues'][i]['name']
    #           i = i+1
    #         else:
    #             pass
    	for venue in herenow:
		venueName=venue['hereNow']['venueName']
		for entry in venue['hereNow']['items']:
			if entry['user']['gender']==gender:
				the_id=entry['user']['id']
				chickpix[the_id]=[entry['user']['photo'][44:],entry['user']['firstName'],venueName]
			else:
				pass
	pairs=[list(x) for x in chunk(chickpix.values(), 4)]
	return render_to_response ('gallery.html', {'chickpix':pairs, 'csrf':params}, context_instance=RequestContext(request))
    

def vote(request):
	authenticator.set_token(request.session['code'])
	pic_id = request.POST['pic_id']
	if rating.objects.filter(pic_id=pic_id).count()==1:
		r1 = rating.objects.get(pic_id=pic_id)
		r1.rating += 1
	else:
		r1 = rating(pic_id=pic_id, rating=1)
	r1.save()
	u1 = user.objects.get(fsq_id=request.session['fsq_id'])
	u1.ratings.add(r1)
        u1.save()
	
	return HttpResponse('Vote successful')
    
    
    
 
    

from django.http import HttpResponse, HttpResponseRedirect 
from django.shortcuts import render_to_response
import pysq.apiv2 as psq
from gallery.models import user, rating
from django.template import RequestContext
from django.core.context_processors import csrf


f = open('/tmp/workfile', 'w')
f.write(psq.__file__)
f.close()

authenticator = psq.FSAuthenticator('H0P2PQASLI5GNXUQSR5KN2MH4Z002YS0VSYNDFS215XNHCY5','HBDVHGLMFXFUT5SXEKLFFGBAYBXJZLGBLQ5BS232F0NGDNRG','http://4sq.getpostd.com/loc/')

# def first(request):
#     HttpResponseRedirect (uri)

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
	da_id=authenticator.query("/users/self")
# 	u1 = user(fsq_id=da_id['user']['id'], contact=da_id['user']['contact'], photo=['user']['photo'][44:])
# 	u1.save()
	request.session['fsq_id']=da_id['user']['id']

	
	trending=authenticator.query("/venues/trending", {'ll':str(lat)+','+str(lon)})
	chickpix={}
	herenow=[]
	i=0
	for item in trending['venues']:
		venue=item['id']
		herenow.append(authenticator.query("/venues/"+venue+"/herenow"))
		herenow[i]['hereNow']['venueName']=trending['venues'][i]['name']
		i = i+1
	for venue in herenow:
		venueName=venue['hereNow']['venueName']
		for user in venue['hereNow']['items']:
			if user['user']['gender']==gender:
				id=user['user']['id']
				chickpix[id]=[user['user']['photo'][44:],user['user']['firstName'],venueName]
			else:
				pass
                     
	return render_to_response ('gallery.html', {'chickpix':chickpix, 'csrf':params}, context_instance=RequestContext(request))
    

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
	u2 = user(ratings=r1)
	u2.save()
	
	return HttpResponse('Vote successful')
    
    
    
 
    

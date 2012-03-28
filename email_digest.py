from time import time
from gallery.models import record, rating, user, user_lookup
import pysq.apiv2 as psq
import settings
from haversine import *

authenticator = psq.FSAuthenticator(settings.CLIENT_ID, settings.CLIENT_SECRET, settings.CALLBACK_URL)


def email(lat,lon, radius):
	recipients=user.objects.filter(last_lat__lt=lat+5, last_lat__gt=lat-5, last_lon__lt=lon+5, last_lon__gt=lon-5)
	recips={}
	for recipient in recipients:
		recips[recipient.fsq_id]=recipient.first_name, recipient.last_name, recipient.email
	the_records = record.objects.filter(time__lt=time(),time__gt=time()-86400)
	the_set={}
	for item in the_records:
		
		v=authenticator.userless_query("/venues/"+item.venue_id)
		vlat=v['venue']['location']['lat']
		vlon=v['venue']['location']['lng']
		venue_name=v['venue']['name']
		try: 
			venue_address=v['venue']['location']['address']+' '+v['venue']['location']['city']+', '+v['venue']['location']['state']+' '+v['venue']['location']['postalCode']
		except:
			pass
		if item.venue_id in the_set.keys():
			the_set[item.venue_id][2]+=item.target.quotient()
			the_set[item.venue_id][3]+=1
		elif haversine(float(vlon),float(vlat),float(lon),float(lat))<=int(radius):
			the_set[item.venue_id]=[venue_name,venue_address,item.target.quotient(),1]
		else:
			pass
	
	averages={}		
	for item in the_set.iteritems():
       		averages[item[0]]=[item[1][2]/item[1][3],{'female':[],'male':[]}]	

	for item in the_records:
		try:

			u=user_lookup.objects.get(pic_id=item.target.pic_id)
			g=authenticator.query("users/"+u.fsq_id, token="1A0ESOQC4W2RIGY442CJTKKFJEM04BYCEHSG0SNCVIWMKPII")
			averages[item.venue_id][1][g['user']['gender']].append(item.target.pic_id)
		except:
			pass
	for item in the_set:
		the_set[item].append(averages[item])
	return the_set, recips

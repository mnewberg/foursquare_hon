from time import time
import operator
from gallery.models import record, user, venue_ll
from haversine import *

def suggested_venues(fsq_id='', lat='', lon='', radius=''):
	newdict = {}
	if fsq_id:
                query = record.objects.filter(time__lt=time(), time__gt=time()-3600, user=user.objects.get(fsq_id=fsq_id)).order_by('venue_id').values('venue_id')
		for venue in query:
	      		if venue['venue_id'] not in newdict:
				newdict[venue['venue_id']]=1              
			else:
				newdict[venue['venue_id']]+=1
	else:
		query = record.objects.filter(time__lt=time(), time__gt=time()-3600).order_by('venue_id').values('venue_id')
		for venue in query:
			v=venue_ll.objects.get(venue_id=venue['venue_id'])
			vlat=v.lat
			vlon=v.lon
			if venue['venue_id'] not in newdict and haversine(float(lat),float(lon),float(vlat),float(vlon)) <= int(radius)/1000:
				newdict[venue['venue_id']]=1
			elif venue['venue_id'] in newdict:
				newdict[venue['venue_id']]+=1
			else:
				pass					   
	sorted_vals=sorted(newdict.iteritems(), key=operator.itemgetter(1))
	sorted_vals.reverse()
	return sorted_vals[:5]

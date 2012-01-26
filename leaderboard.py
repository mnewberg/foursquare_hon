from time import time
import operator
from gallery.models import record, user

def suggested_venues(fsq_id):
	newdict = {}
	for venue in record.objects.filter(time__lt=time(), time__gt=time()-3600, user=user.objects.get(fsq_id=fsq_id)).order_by('venue_id').values('venue_id'):
		if venue['venue_id'] not in newdict:
			newdict[venue['venue_id']]=1               
		else:
			newdict[venue['venue_id']]+=1
	sorted_vals=sorted(newdict.iteritems(), key=operator.itemgetter(1))
	sorted_vals.reverse()
	return sorted_vals[:5]
	
	
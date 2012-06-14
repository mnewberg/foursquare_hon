import datetime
import pysq.apiv2 as psq
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from twilio.rest import TwilioRestClient
import settings
from models import routing, avail_DIDs, log
from gallery.models import user, twitter_outreach, user_lookup
from time import time
from django.shortcuts import render_to_response
import re

client = TwilioRestClient(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
authenticator = psq.FSAuthenticator(settings.CLIENT_ID, settings.CLIENT_SECRET, settings.CALLBACK_URL)

def transcribe(request):
	sid=request.POST['TranscriptionSid']
	text=request.POST['TranscriptionText']
	url=request.POST['RecordingUrl']
	print sid, text, url
	return HttpResponse('ok')

def simon2(request):
	client.calls.create(from_="+13109123101", to="+14158952957", url="http://staging.tryfourplay.com/static/play.xml")
	return HttpResponse('ok')

def simon(request):
	return render_to_response('simon2.html')

def xml(request):
	voice=request.GET['voice']
	text=re.sub(' ','%20',request.GET['text'])
	document=open('/var/www/four_staging/foursquare/static/media/test.xml','w')
	document.write("""<?xml version=\"1.0\" encoding=\"utf-8\"?><Response>
<Play>http://api.ispeech.org/api/rest?apikey=44ce84e83a1f4e7f676d058a3f6c921a&amp;action=convert&amp;text="""+text+"""&amp;voice="""+voice+"""&amp;format=wav</Play>
</Response>""")
	document.close()
	return HttpResponse('done')


def advanceDID(phone):
        try:
		current_did=routing.objects.filter(recipient=phone).count()
		new_did_id=current_did+1
		curr_did=avail_DIDs.objects.get(id=new_did_id)
		return curr_did
	except:
		pass

def callback(request):
	f_id=request.session['fsq_id']
	request.session.set_expiry(datetime.datetime(2012, 12, 12, 0, 0))
	try: 
		uid=request.session['uid']
	except:
		uid=twitter_outreach.objects.filter(m_target=user_lookup.objects.get(fsq_id=f_id), read=False)[0].uid
		return HttpResponseRedirect("/message/"+uid)
	outreach=twitter_outreach.objects.get(uid=uid)
	outreach.read=True
	outreach.save()
	logged_in_user=user.objects.get(fsq_id=f_id)
	other_user=user.objects.get(fsq_id=outreach.sender)
	for i in [(logged_in_user.phone, other_user.phone),(other_user.phone,logged_in_user.phone)]:
		if routing.objects.filter(sender=i[1]).count()>0:
			curr_did=advanceDID(i[1])
		else:
			curr_did=avail_DIDs.objects.get(id=1)
		routing.objects.create(recipient=i[0],sender=i[1],DID=curr_did, time_created=round(time()))
	request.session['curr_did']=curr_did
	request.session['logged_in']=logged_in_user.phone
	## message=client.sms.messages.create(to=logged_in_user.phone, from_=curr_did, body="Fourplay here. Please wait while we grab your secret admirerer!")

   ## now sms the initiator

	if routing.objects.filter(sender=logged_in_user.phone).count()>1:
		curr_outgoing_did=advanceDID(logged_in_user.phone)
	else:
		curr_outgoing_did=avail_DIDs.objects.get(id=1)
	request.session['curr_outgoing_did']=curr_outgoing_did
	request.session['other_user']=other_user.phone
	request.session['other_user_name']=other_user.first_name
	request.session['logged_in_name']=logged_in_user.first_name
	#message=client.sms.messages.create(to=other_user.phone, from_=curr_outgoing_did,body=logged_in_user.first_name + " is waiting to play with you at http://staging.tryfourplay.com/game/"+uid)
	game_id=twitter_outreach.objects.get(uid=uid).game.gid
	return render_to_response('game.html', {'channel_id':uid,'game_id':game_id})

@csrf_exempt
def incoming(request):
	sender=request.POST['From']
	did=avail_DIDs.objects.get(DID=request.POST['To'])
	the_message=request.POST['Body']
	the_recipient=routing.objects.get(sender=sender,DID=did).recipient
	recipient_did=routing.objects.get(sender=the_recipient,recipient=sender).DID.DID
	message=client.sms.messages.create(to=the_recipient, from_=recipient_did, body=the_message)
	log.objects.create(time=time(),sender=sender,recipient=the_recipeint,from_did=recipient_did, to_did=the_recipient, message=the_message)
	return HttpResponse('success')

def endgame(request):
	curr_did=request.session['curr_did']
	logged_in=request.session['logged_in']
	curr_outgoing_did=request.session['curr_outgoing_did']
	try:
		other_user=request.session['other_user']
		other_user_name=request.session['other_user_name']
		logged_in_name=request.session['logged_in_name']
	except:
		return HttpResponse('fail')
	winner=request.GET['victory']
	locations=twitter_outreach.objects.get(uid=request.session['uid'])
	logged_in_vid=locations.venue_id
	other_user_vid=locations.other_venue_id
	venue_names=[]
	for i in [logged_in_vid,other_user_vid]:
		v=authenticator.userless_query("/venues/"+i)
		venue_names.append(v['venue']['name'])
	if winner=='true':
		logged_in_status='won!!'
		other_user_status='lost :( . How about buying '+logged_in_name+' a drink at '+venue_names[0]+'?'
	else:
		logged_in_status='lost :( . How about buying '+other_user_name+' a drink at '+venue_names[1]+'?'
		other_user_status='won!!1'

	message=client.sms.messages.create(to=logged_in, from_=curr_did, body="Game over, you " +logged_in_status)
	message2=client.sms.messages.create(to=other_user, from_=curr_outgoing_did,body="Game over, you "+other_user_status)
	return HttpResponse('success')

def nudge(request):
	uid=request.GET['uid']
	t=twitter_outreach.objects.get(uid=uid)
	logged_in_user=user.objects.get(fsq_id=t.m_target.fsq_id)
	other_user=t.sender
	if 'uid' not in request.session:	
		outgoing=routing.objects.get(recipient=logged_in_user.phone,sender=other_user.phone)
		message=client.sms.messages.create(to=logged_in_user.phone, from_=outgoing.DID.DID,body=other_user.first_name + " is waiting to play with you at http://staging.tryfourplay.com/game/"+uid)
		status='ok'
		print status
	else:
		outgoing=routing.objects.get(recipient=other_user.phone,sender=logged_in_user.phone)
		message=client.sms.messages.create(to=other_user.phone, from_=outgoing.DID.DID,body=logged_in_user.first_name + " is waiting to play with you at http://staging.tryfourplay.com/game/"+uid)
	return HttpResponse(status)

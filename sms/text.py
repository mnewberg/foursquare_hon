from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from twilio.rest import TwilioRestClient
import settings
from models import routing, avail_DIDs, log
from gallery.models import user, twitter_outreach, user_lookup
from time import time
from django.shortcuts import render_to_response
client = TwilioRestClient(settings.ACCOUNT_SID,settings.AUTH_TOKEN)



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

	message=client.sms.messages.create(to=other_user.phone, from_=curr_outgoing_did,body=logged_in_user.first_name + " wants to play with you at http://staging.tryfourplay.com/game/"+uid)
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
	other_user=request.session['other_user']
	message=client.sms.messages.create(to=logged_in, from_=curr_did, body="game ova")
	message2=client.sms.messages.create(to=other_user, from_=curr_outgoing_did,body="game ova")
	return HttpResponse('success')

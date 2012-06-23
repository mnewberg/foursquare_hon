from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import render_to_response
import json
import pusher
from gallery.models import twitter_outreach, user, user_lookup

from collections import OrderedDict
import random

pusher.app_id='19318'
pusher.key='890abd57f862ab2712ff'
pusher.secret='00d5dd3756b1594826f2'

@csrf_exempt
def auth(request):
    p = pusher.Pusher()
    socket = request.POST['socket_id']
    channel = request.POST['channel_name']
    daresponse = p[channel].authenticate(socket,{'user_id':random.randint(1,999999999)})
    return HttpResponse(json.dumps(daresponse))

def game(request, uid):
    outreach=twitter_outreach.objects.get(uid=uid)
    game_id=outreach.game.gid
    user1=outreach.sender
    user2=user.objects.get(fsq_id=outreach.m_target.fsq_id)
    user1_name=user1.first_name
    user1_pic=user1.photo
    user2_pic=user2.photo
    user2_name=user2.first_name
    return render_to_response("newgame.html", {'channel_id':uid,'game_id':game_id,'user1_pic':user1_pic,'user1_name':user1_name,'user2_pic':user2_pic,'user2_name':user2_name})

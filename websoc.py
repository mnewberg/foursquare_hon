from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import render_to_response
import json
import pusher

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

def game(request):
    return render_to_response("game.html")

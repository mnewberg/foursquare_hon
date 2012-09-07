from django.conf.urls.defaults import patterns, include, url
import views
import pysq.apiv2 as psq
from django.views.generic.simple import redirect_to
from django.contrib import admin
admin.autodiscover()
import websoc

from websoc import *
from ajaxreqs import ajaxreq
authenticator = psq.FSAuthenticator('W1EKUBNDSX3ROZJB5HCIIDZPIHNM5FPUSEYWW03GA5WTLC0G','TN2N44EY3SQ0M43TIV2KZKDH5NKHJ4ROWM5Z5W0G1KL1UXEP','http://tryfourplay.com/loc/')

uri = authenticator.authorize_uri()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$','views.home'),
    url(r'^instagram',redirect_to,{'url':'instagram://user?username=tlimongello'}),
    url(r'^favicon.ico',redirect_to, {'url':'http://c15075740.r40.cf2.rackcdn.com/favicon.ico'}),
    url(r'^faq$','views.faq'),
    url(r'^hook$','views.hook'),
    url(r'^tos$','views.tos'),
    url(r'^login$','views.login'),
    url(r'^loc/$','views.second'),
    # url(r'^newgallery$','ajaxreqs.newgallery'),
    url(r'^fsq$','ajaxreqs.ajaxreq'),
    url(r'^getpage$','ajaxreqs.get_page'),
    url(r'^message/(.{1,5})','views.onboard'),
    url(r'^checkin$','views.checkin'),
    url(r'^outreach$','views.outreach'),
    url(r'^pickmessage/$','views.pickmessage'),
    url(r'^updatetwitter/$','views.updatetwitter'),
    url(r'^phone/$','views.missing_sender'),
    url(r'^callback$','sms.text.callback'),
    url(r'^incoming$','sms.text.incoming'),
    url(r'^missing$','views.missing'),
    url(r'^unsub/$','views.unsubscribe'),
    url(r'^block/$','views.block'),
    url(r'^git/$','views.postrecv'),
    # Examples:
    # url(r'^$', 'twilio.views.home', name='home'),
    # url(r'^twilio/', include('twilio.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^pusher/auth','websoc.auth'),
     url(r'^game/(.{1,5})','websoc.game'),
     url(r'^nudge$','sms.text.nudge'),
     url(r'^textall$','sms.text.endgame'),
     url(r'^admin/', include(admin.site.urls)),
)

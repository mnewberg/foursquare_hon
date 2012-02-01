from django.conf.urls.defaults import patterns, include, url
import views
import pysq.apiv2 as psq
from django.views.generic.simple import redirect_to


authenticator = psq.FSAuthenticator('H0P2PQASLI5GNXUQSR5KN2MH4Z002YS0VSYNDFS215XNHCY5','HBDVHGLMFXFUT5SXEKLFFGBAYBXJZLGBLQ5BS232F0NGDNRG','http://4sq.getpostd.com/loc/')

uri = authenticator.authorize_uri()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',redirect_to,{'url':uri}),
    url(r'^loc/$','views.second'),
    url(r'^gallery/(\d{1,3})$','views.gallery'),
    url(r'^rating/$','views.vote'),
    url(r'^postrecv/$','views.postrecv'),
    url(r'^results/$','views.results'),
    url(r'^dialog/(.*|\.jpg|\.png|\.gif|\.jpeg)', 'views.dialog'),
    url(r'^notice','views.notice'),
    # Examples:
    # url(r'^$', 'twilio.views.home', name='home'),
    # url(r'^twilio/', include('twilio.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

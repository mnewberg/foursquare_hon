from django.contrib import admin
from gallery.models import *
from sms.models import routing,avail_DIDs,log


class userAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','last_lat','last_lon','date_joined','twitter')
    list_filter = ('date_joined',)

class user_lookupAdmin(admin.ModelAdmin):
    list_display=('pic_id','t_handle')
    filter_horizontal=('blocks',)
    
class routingAdmin(admin.ModelAdmin):
    list_display=('sender','recipient','DID')
    list_filter=('sender','DID',)

class twitter_outreachAdmin(admin.ModelAdmin):
    list_display=('m_target','sender','uid','message','game','venue_id','other_venue_id','read')
    raw_id_fields = ('m_target',)

admin.site.register(user, userAdmin)
admin.site.register(venue_ll)
admin.site.register(user_lookup, user_lookupAdmin)
admin.site.register(invite_codes)
admin.site.register(twitter_outreach, twitter_outreachAdmin)
admin.site.register(game)
admin.site.register(routing, routingAdmin)
admin.site.register(avail_DIDs)
admin.site.register(log)
admin.site.register(queue)

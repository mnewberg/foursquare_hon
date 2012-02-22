from django.contrib import admin
from gallery.models import user, record, rating, venue_ll, user_lookup, invite_codes



class userAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','date_joined','twitter')
    list_filter = ('date_joined',)
    filter_horizontal=('records',)

class recordAdmin(admin.ModelAdmin):
    list_display=('venue_id','time')
    list_filter=('time',)


admin.site.register(user, userAdmin)
admin.site.register(record, recordAdmin)
admin.site.register(rating)
admin.site.register(venue_ll)
admin.site.register(user_lookup)
admin.site.register(invite_codes)

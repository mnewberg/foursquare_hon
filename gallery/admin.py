from django.contrib import admin
from gallery.models import user, record, rating, venue_ll, user_lookup, invite_codes

admin.site.register(user)
admin.site.register(record)
admin.site.register(rating)
admin.site.register(venue_ll)
admin.site.register(user_lookup)
admin.site.register(invite_codes)

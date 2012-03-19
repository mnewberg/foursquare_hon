from django_cron import cronScheduler, Job
from time import time, sleep
from twilio.rest import TwilioRestClient
from sms.models import routing
import settings
import commands
from urllib import urlretrieve
import pysq.apiv2 as psq
import cloudfiles

client = TwilioRestClient(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
authenticator = psq.FSAuthenticator(settings.CLIENT_ID, settings.CLIENT_SECRET, settings.CALLBACK_URL)
token='1A0ESOQC4W2RIGY442CJTKKFJEM04BYCEHSG0SNCVIWMKPII'
conn=cloudfiles.get_connection('thenewb','9eddf4532803a3ab2f813773c5514803')

class ExpireRoutes(Job):

    # run every 3000 seconds (5 minutes)
    run_every = 750

    def job(self):
        # This will be executed ever 5 mins
        to_expire=routing.objects.filter(time_created__lt=time()-1800)


        for item in to_expire:
            client.sms.messages.create(to=item.recipient,from_=item.DID,body="*Message from Fourplay* Wrap it up! Your conversation will end in 5 minutes.")
            
        sleep(300)
        for item in to_expire:
            item.delete()
cronScheduler.register(ExpireRoutes)

#class AusGrab(Job):
#    run_every = 300
#    
#    def job(self):
#        now=authenticator.query("/venues/440da2cbf964a52091301fe3/herenow",token)
#        contain=conn.get_container('fourplay')
#        objects=contain.get_objects()
#        for item in now['hereNow']['items']:
#            if item['user']['photo'][44:] not in objects:
#                commands.getoutput('wget https://img-s.foursquare.com/userpix/'+item['user']['photo'][44:]+' -P /var/www/four_staging/foursquare/static/media')
#                commands.getoutput('mogrify -thumbnail 160 /var/www/four_staging/foursquare/static/media/'+ item['user']['photo'][44:])
#                img=contain.create_object(item['user']['photo'][44:])
#                img.load_from_file('/var/www/four_staging/foursquare/static/media'+item['user']['photo'][44:])
#                f='/var/www/four_staging/foursquare/static/media/'+item['user']['photo'][44:]
#                img.load_from_filename(f)
#            else:
#                pass

#cronScheduler.register(AusGrab)

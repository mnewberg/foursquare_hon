from time import time, sleep
from twilio.rest import TwilioRestClient
from sms.models import routing
import settings
import commands


client = TwilioRestClient(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
to_expire=routing.objects.filter(time_created__lt=time()-1800)
print to_expire
for item in to_expire:
    client.sms.messages.create(to=item.recipient,from_=item.DID,body="*Message from Fourplay* Wrap it up! Your conversation will end in 5 minutes.")
sleep(300)
for item in to_expire:
    item.delete()


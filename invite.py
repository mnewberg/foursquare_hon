from gallery.models import queue
from sendemail import approval_email

def send_invite(quota):
    chosen=queue.objects.all()[:quota]
    for item in chosen:
        approval_email(item.email, item.allocated_invite.code, item.first_name)
        item.delete()
    return 'success'

def send_filter(queue_objects):
    for item in queue_objects:
        approval_email(item.email, item.allocated_invite.code, item.first_name)
        item.delete()
    return 'success'

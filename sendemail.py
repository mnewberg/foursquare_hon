from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from email_digest import htmlemail

def sendmessage(email):
    htmly= get_template('email.html')
    test=htmlemail(40.721786,-74.009447,3)
    d = Context({ 'dadict':test })

    subject, from_email, to = 'hello', 'matt@tryfourplay.com', email
    text_content = 'PLAIN TEXT NOT AVAILABLE'
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return 'Success'


def queue_email(email,first_name):
    html=get_template('queue_email.html')
    d = Context({'first_name':first_name})
    subject, from_email, to = 'Thanks for Joining the playdo.pe Waiting List', 'playdo.pe<dopebot@playdo.pe>',email
    html_content= html.render(d)
    text_content='Thanks for joining the playdo.pe waiting list. We\'ll be in touch soon. In the meantime follow us on twitter @playdope. We\'re excited to get you playing soon!'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content,"text/html")
    msg.send()
    return 'Success'

def approval_email(email, invite_code, first_name):
    html=get_template('approval_email.html')
    d = Context({'first_name':first_name, 'invite_code':invite_code})
    subject, from_email, to = 'You\'ve Been Invited to Join playdo.pe', 'playdo.pe<dopebot@playdo.pe>',email
    html_content= html.render(d)
    text_content='Congrats! You\'ve been invited to join playdo.pe! Copy and paste the following link into your browser bar: http://playdo.pe/login?invite_code={{invite_code}}'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content,"text/html")
    msg.send()
    return 'Success'

def welcome_email(email, first_name):
    html=get_template('welcome_email.html')
    d = Context({'first_name':first_name, 'email':email})
    subject, from_email, to = 'Welcome to playdo.pe!', 'playdo.pe<dopebot@playdo.pe>',email
    html_content= html.render(d)
    text_content='Welcome to playdo.pe!'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content,"text/html")
    msg.send()
    return 'Success'
    

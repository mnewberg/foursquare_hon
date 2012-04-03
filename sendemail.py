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

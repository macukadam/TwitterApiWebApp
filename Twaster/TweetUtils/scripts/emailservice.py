from django.core.mail import EmailMessage

def sendmail(usermail,location):
    email = EmailMessage('Twasterbot Alert!!!', 'Earthquake detected in {0} at {1}'.format(location,"time"), to=[usermail])
    email.send()
from django.core.mail import send_mail
from django.conf import settings

class sendmail:
    subject = None
    message = None
    from_ = None
    to_ = None
    def __init__(self, subject, message, from_, to_) -> None:
        self.subject = subject
        self.message = message 
        self.from_ = from_
        self.to_ = to_
    
    
    def _send(self):
        send_mail(subject=self.subject, message=self.message, from_email=self.from_, recipient_list=[self.to_], fail_silently=False)
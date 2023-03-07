from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    body = models.CharField(max_length=2500)
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="received_messaged")
    time_sent = models.DateTimeField(auto_now=True)

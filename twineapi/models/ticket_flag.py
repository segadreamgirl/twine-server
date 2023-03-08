from django.db import models
from .ticket import Ticket 
from .flag import Flag

class TicketFlag(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="ticket_flags")
    flag = models.ForeignKey(Flag, on_delete=models.CASCADE)
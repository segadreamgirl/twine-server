from django.db import models
from django.contrib.auth.models import User
from .project import Project


class Ticket(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_tickets")
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    completed = models.BooleanField(default=False)
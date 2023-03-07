from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    title = models.CharField(max_length=100)
    deadline = models.DateField(null=True)
    lead = models.ForeignKey(User, on_delete=models.CASCADE, related_name="project_lead")

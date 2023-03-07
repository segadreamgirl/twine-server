from django.db import models


class Flag(models.Model):
    name = models.CharField(max_length=150)
    color = models.CharField(max_length=50)

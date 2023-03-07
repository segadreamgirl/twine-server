from django.db import models
from django.contrib.auth.models import User
from .project import Project


class ProjectTeam(models.Model):
    employee = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, related_name="number_of_projects")

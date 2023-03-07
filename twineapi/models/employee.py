from django.db import models
from django.contrib.auth.models import User
from .department import Department

class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee_account")
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    profile_pic = models.CharField(max_length=2000)

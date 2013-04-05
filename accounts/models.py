from django.db import models
from django.contrib.auth.models import User
from problems.models import Problem

class Profile(models.Model):
    user = models.OneToOneField(User)
    
    problem_solved = models.ManyToManyField(Problem, blank=True)
    nick_name = models.CharField(blank=True,max_length=100)
    school = models.CharField(blank=True,max_length=100)
    motto = models.CharField(blank=True,max_length=100)
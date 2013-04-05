from django.db import models
from django.contrib.auth.models import User
from problems.models import Problem

class Submission(models.Model):
    problem = models.ForeignKey(Problem)
    user = models.ForeignKey(User)
    source_code = models.CharField(max_length=100000)
    status = models.CharField(max_length=50)
    datetime = models.DateTimeField()
    language = models.CharField(max_length=20)
    time_cost = models.IntegerField()
    memory_cost = models.IntegerField()
     
    def __unicode__(self):
        return "Submission #" + str(self.pk)
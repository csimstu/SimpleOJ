from django.db import models

class Problem(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    input_format = models.TextField()
    output_format = models.TextField()
    note = models.TextField(blank=True)
    time_limit = models.IntegerField()
    memory_limit = models.IntegerField()
    
    def __unicode__(self):
        return self.title

class TestCase(models.Model):
    input = models.TextField()
    output = models.TextField()
    problem = models.ForeignKey(Problem)
    is_sample = models.BooleanField()
    is_for_judge = models.BooleanField()
from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    details = models.TextField()
    target = models.DecimalField(max_digits=10, decimal_places=1)
    start_date = models.DateField()
    end_date = models.DateField()
    def __str__(self):
        return self.title


from django.db import models

# Create your models here.
class Climate(models.Model):
    name=models.CharField(max_length=150)
    date=models.DateField()
    temperature=models.IntegerField(max_length=50)

class Meta:
    ordering =('name',)
from django.db import models

# Create your models here.


class Container(models.Model):
   # id = models.IntegerField(primary_key=True,auto_created=True)
    datetime = models.DateTimeField(auto_now=True)
    #unique = models.CharField(max_length=40, unique=True)
    namespace = models.CharField(max_length=100)
    podname = models.CharField(max_length=100)
    containername = models.CharField(max_length=100)

    def __str__(self):
        return self.containername

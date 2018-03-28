from django.db import models

# Create your models here.


class HomeAppModel(models.Model):
    name = models.CharField(max_length=100,null=False)


from django.db import models
from django.contrib.auth.models import User



class Deal(models.Model):
    customer = models.CharField(max_length=20)
    item = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.customer}-{self.item}"

class Richuser(models.Model):
    username=models.CharField(max_length=20)
    spent_money=models.DecimalField(max_digits=10, decimal_places=2)
    gems=models.CharField(max_length=200)

    def __str__(self):
        return f"{self.username}"








from django.db import models
from users.models import User

class Equipment(models.Model):
    name = models.CharField(max_length=200)
    inventory_number = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=100)
    purchase_date = models.DateField()
    status = models.CharField(max_length=50)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class Maintenance(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    performed_by = models.CharField(max_length=200)

class Stock(models.Model):
    item_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    minimum_quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
from django.db import models
from student.models import Student

class Account(models.Model):
    number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=12, decimal_places=2)

class Transaction(models.Model):
    date = models.DateField()
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=50)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

class SchoolFee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=50)
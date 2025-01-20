from django.db import models
from users.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    available_quantity = models.PositiveIntegerField()
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=50)

class BookLoan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
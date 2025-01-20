from rest_framework import serializers
from .models import Book, BookLoan

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BookLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookLoan
        fields = '__all__'


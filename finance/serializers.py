from rest_framework import serializers
from .models import Account, Transaction, SchoolFee

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class SchoolFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolFee
        fields = '__all__'


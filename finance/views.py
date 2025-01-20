from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Account, Transaction, SchoolFee
from .serializers import AccountSerializer, TransactionSerializer, SchoolFeeSerializer

class AccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les comptes.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    
    @action(detail=True)
    def transactions(self, request, pk=None):
        """Retourne les transactions d'un compte."""
        account = self.get_object()
        transactions = account.transaction_set.all()
        return Response(TransactionSerializer(transactions, many=True).data)
    
class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les comptes.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    
    @action(detail=False)
    def incomes(self, request, pk):
        """Retourne les transactions entrantes."""
        transactions = self.get_object()
        incomes = transactions.filter(type=pk)
        return Response(TransactionSerializer(incomes, many=True).data)
    
    @action(detail=False)
    def expenses(self, request, pk):
        """Retourne les transactions sortantes."""
        transactions = self.get_object()
        expenses = transactions.filter(type=pk)
        return Response(TransactionSerializer(expenses, many=True).data)
    
class SchoolFeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les frais scolaires.
    """
    queryset = SchoolFee.objects.all()
    serializer_class = SchoolFeeSerializer
    
    @action(detail=True)
    def student(self, request, pk=None):
        """Retourne les frais scolaires d'un étudiant."""
        school_fee = self.get_object()
        return Response(SchoolFeeSerializer(school_fee).data)
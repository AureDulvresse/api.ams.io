from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Book, BookLoan
from .serializers import BookSerializer, BookLoanSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les livres.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    @action(detail=True, methods=['post'])
    def loan(self, request, pk=None):
        """Prêter un livre à un utilisateur."""
        book = self.get_object()
        # Logique de prêt
        return Response({'status': 'book loaned'})

class BookLoanViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les prêts de livres.
    """
    queryset = BookLoan.objects.all()
    serializer_class = BookLoanSerializer
    
    
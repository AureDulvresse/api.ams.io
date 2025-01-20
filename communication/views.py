from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Message, Announcement
from .serializers import MessageSerializer, AnnouncementSerializer

class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les messages.
    
    list:
    Retourne la liste des messages de l'utilisateur.
    
    create:
    Envoie un nouveau message.
    
    retrieve:
    Retourne les détails d'un message spécifique.
    
    update:
    Met à jour un message existant.
    
    destroy:
    Supprime un message existant.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        """Filtre les messages pour l'utilisateur courant."""
        user = self.request.user
        return Message.objects.filter(recipient=user) | Message.objects.filter(sender=user)
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Marquer un message comme lu."""
        message = self.get_object()
        message.mark_as_read()
        return Response({'status': 'message marked as read'})

class AnnouncementViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les annonces.
    
    list:
    Retourne la liste des annonces.
    
    create:
    Crée une nouvelle annonce.
    
    retrieve:
    Retourne les détails d'une annonce spécifique.
    
    update:
    Met à jour une annonce existante.
    
    destroy:
    Supprime une annonce existante.
    """
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    
    @action(detail=False)
    def recent(self, request):
        """Retourne les annonces récentes."""
        recent_announcements = Announcement.objects.order_by('-publish_date')[:5]
        serializer = self.get_serializer(recent_announcements, many=True)
        return Response(serializer.data)

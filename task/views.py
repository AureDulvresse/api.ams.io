from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task, TaskComment
from .serializers import TaskSerializer, TaskCommentSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les tâches.
    
    list:
    Retourne la liste des tâches.
    
    create:
    Crée une nouvelle tâche.
    
    retrieve:
    Retourne les détails d'une tâche spécifique.
    
    update:
    Met à jour une tâche existante.
    
    destroy:
    Supprime une tâche existante.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        """Filtre les tâches selon l'utilisateur."""
        user = self.request.user
        return Task.objects.filter(assigned_to=user) | Task.objects.filter(created_by=user)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Marquer une tâche comme terminée."""
        task = self.get_object()
        task.mark_as_completed()
        return Response({'status': 'task marked as completed'})
    
    @action(detail=True)
    def comments(self, request, pk=None):
        """Retourne les commentaires d'une tâche."""
        task = self.get_object()
        comments = task.taskcomment_set.all()
        serializer = TaskCommentSerializer(comments, many=True)
        return Response(serializer.data)

class TaskCommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les commentaires des tâches.
    """
    queryset = TaskComment.objects.all()
    serializer_class = TaskCommentSerializer

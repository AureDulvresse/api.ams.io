import datetime
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Room, ScheduleEntry
from .serializers import RoomSerializer, ScheduleEntrySerializer

class ScheduleEntryViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les emplois du temps.
    """
    queryset = ScheduleEntry.objects.all()
    serializer_class = ScheduleEntrySerializer
    
    @action(detail=False)
    def weekly(self, request):
        """Retourne l'emploi du temps hebdomadaire."""
        # Logique de récupération de l'emploi du temps [TO_DO]
        return Response({'schedule': 'weekly schedule data'})
    
    @action(detail=False)
    def daily(self, request):
      """Retourner l'emploi du temps journalier."""
      today = datetime.date.today()
      schedule = ScheduleEntry.objects.filter(day_of_week=today.weekday(), start_time__date=today)
      return Response(ScheduleEntrySerializer(schedule, many=True).data)
    
class RoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les salles de classe et espace d'activité.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

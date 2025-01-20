from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Equipment, Maintenance, Stock
from .serializers import EquipmentSerializer, MaintenanceSerializer, StockSerializer

class EquipmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les équipements.
    """
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    
    @action(detail=True)
    def maintenance_history(self, request, pk=None):
        """Retourne l'historique de maintenance d'un équipement."""
        equipment = self.get_object()
        maintenance = equipment.maintenance_set.all()
        return Response(MaintenanceSerializer(maintenance, many=True).data)

class MaintenanceViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les maintenance.
    """
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer

class StockViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer le stock.
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Employee, Leave, Salary
from .serializers import EmployeeSerializer, LeaveSerializer, SalarySerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les employés.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    
    @action(detail=True)
    def leaves(self, request, pk=None):
        """Retourne les congés de l'employé."""
        employee = self.get_object()
        leaves = employee.leave_set.all()
        return Response(LeaveSerializer(leaves, many=True).data)
    
    
class LeaveViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les employés.
    """
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    
    @action(detail=True)
    def agree(self, request, pk=None):
        """Accorder un congé à un employé."""
        leave = self.get_object()
        leave.status = 'agreed'
        leave.save()

        return Response({'leave': leave})

        
class SalaryViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les employés.
    """
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    
    @action(detail=True)
    def paid(self, request, pk=None):
        """Payer un employé."""
        salary = self.get_object()
        salary.is_paid = True
        salary.save()

        return Response({'paid': salary})
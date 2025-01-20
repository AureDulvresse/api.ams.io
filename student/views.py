from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Student, Grade, Attendance
from .serializers import StudentSerializer, GradeSerializer, AttendanceSerializer

class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les étudiants.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    @action(detail=True)
    def grades(self, request, pk=None):
        """Retourne les notes de l'étudiant."""
        student = self.get_object()
        grades = student.grade_set.all()
        return Response(GradeSerializer(grades, many=True).data)
    
    @action(detail=True)
    def attendance(self, request, pk=None):
        """Retourne les présences de l'étudiant."""
        student = self.get_object()
        attendance = student.attendance_set.all()
        return Response(AttendanceSerializer(attendance, many=True).data)

class GradeViewSet(viewsets.ModelViewSet):
   """
   API endpoint pour gérer les notes
   """
   queryset = Grade.objects.all()
   serializer_class = GradeSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les absences
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
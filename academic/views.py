from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.serializers import UserSerializer
from student.serializers import GradeSerializer
from .models import AcademicYear, ClassGroup, Course, CourseMaterial
from .serializers import (AcademicYearSerializer, ClassGroupSerializer,
                        CourseSerializer, CourseMaterialSerializer)

class AcademicYearViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les années académiques.
    """
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    
    @action(detail=True, methods=['post'])
    def set_current(self, request, pk=None):
        """Définit l'année académique courante."""
        year = self.get_object()
        AcademicYear.objects.all().update(is_current=False)
        year.is_current = True
        year.save()
        return Response({'status': 'current year set'})

class ClassGroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les classes.
    """
    queryset = ClassGroup.objects.all()
    serializer_class = ClassGroupSerializer
    
    @action(detail=True)
    def students(self, request, pk=None):
        """Retourne la liste des étudiants d'une classe."""
        class_group = self.get_object()
        students = class_group.student_set.all()
        return Response(StudentSerializer(students, many=True).data)
    
class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les cours.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    @action(detail=True)
    def teachers(self, request, pk=None):
        """Retourne la liste des professeurs attachés à un cours."""
        course = self.get_object()
        teachers = course.teacher_set.all()
        return Response(UserSerializer(teachers, many=True).data)
    
    @action(detail=True)
    def grades(self, request, pk=None):
        """Retourne la liste des notes obtenues pour un cours."""
        course = self.get_object()
        grades = course.grade_set.all()
        return Response(GradeSerializer(grades, many=True).data)

    @action(detail=True)
    def grades_per_teacher(self, request, pk):
        """Retourne la liste des notes obtenues pour un cours par professeur."""
        course = self.get_object()
        teacher_course = course.teacher_set.filter(pk)
        grades = teacher_course.grade_set.all()
        return Response(GradeSerializer(grades, many=True).data)

class CourseMaterialViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les matériels de cours.
    """
    queryset = CourseMaterial.objects.all()
    serializer_class = CourseMaterialSerializer
    
    @action(detail=True)
    def courses(self, request, pk=None):
        """Retourne la liste des professeurs attachés à un cours."""
        course_materials = self.get_object()
        courses = course_materials.course_set.all()
        return Response(CourseSerializer(courses, many=True).data)
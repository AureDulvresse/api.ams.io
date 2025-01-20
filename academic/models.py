from django.db import models
from users.models import User

class AcademicYear(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

class ClassGroup(models.Model):
    name = models.CharField(max_length=100)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    head_teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    capacity = models.PositiveIntegerField()

class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    credits = models.PositiveIntegerField()
    class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE)
    teachers = models.ManyToManyField(User)
    syllabus = models.FileField(upload_to='syllabi/', null=True, blank=True)

class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='course_materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
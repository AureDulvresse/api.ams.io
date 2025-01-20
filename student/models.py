from django.db import models
from users.models import User
from academic.models import ClassGroup, Course

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    current_class = models.ForeignKey(ClassGroup, on_delete=models.SET_NULL, null=True)
    enrollment_date = models.DateField(auto_now_add=True)
    parents = models.ManyToManyField(User, related_name='children')

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=50)
    coefficient = models.DecimalField(max_digits=3, decimal_places=2, default=1.0)
    remarks = models.TextField(blank=True)

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField()
    justification = models.TextField(blank=True)
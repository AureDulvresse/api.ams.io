from django.db import models
from academic.models import Course
from users.models import User

class Room(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()
    equipment = models.TextField(blank=True)

class ScheduleEntry(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    day_of_week = models.PositiveIntegerField()
    recurrent = models.BooleanField(default=True)
from django.db import models
from users.models import User

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='created_tasks', on_delete=models.CASCADE)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=50)
    priority = models.CharField(max_length=20)
    completion_date = models.DateTimeField(null=True, blank=True)

class TaskComment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
from django.contrib import admin
from hr.models import Employee, Leave, Salary

admin.site.register(Employee)
admin.site.register(Leave)
admin.site.register(Salary)
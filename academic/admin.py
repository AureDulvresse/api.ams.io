from django.contrib import admin
from academic.models import AcademicYear, ClassGroup, Course, CourseMaterial

admin.site.register(AcademicYear)
admin.site.register(ClassGroup)
admin.site.register(Course)
admin.site.register(CourseMaterial)
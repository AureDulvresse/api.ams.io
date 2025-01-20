from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'academic-years', views.AcademicYearViewSet)
router.register(r'class-groups', views.ClassGroupViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'course-materials', views.CourseMaterialViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
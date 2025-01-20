from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'employees', views.EmployeeViewSet)
router.register(r'leaves', views.LeaveViewSet)
router.register(r'salaries', views.SalaryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
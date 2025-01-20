from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'equipment', views.EquipmentViewSet)
router.register(r'maintenance', views.MaintenanceViewSet)
router.register(r'stock', views.StockViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
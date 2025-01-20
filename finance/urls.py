from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'accounts', views.AccountViewSet)
router.register(r'transactions', views.TransactionViewSet)
router.register(r'school-fees', views.SchoolFeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
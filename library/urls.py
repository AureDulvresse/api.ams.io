from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'loans', views.BookLoanViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
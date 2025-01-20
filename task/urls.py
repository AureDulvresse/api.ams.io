from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet)
router.register(r'comments', views.TaskCommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import CustomTokenObtainPairView
from . import views

router = DefaultRouter()
router.register(r'profile', views.UserProfileViewSet, basename='profile')
router.register(r'auth', views.AuthViewSet, basename='auth')
router.register(r'documents', views.UserDocumentViewSet, basename="documents")

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
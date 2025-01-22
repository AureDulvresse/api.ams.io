from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
from django.contrib.auth import get_user_model
import uuid
import resend
from datetime import datetime
from django.utils import timezone
from users.serializers import (CustomTokenObtainPairSerializer, RegisterSerializer,
    UserDocumentSerializer)
from users.models import UserDocument

User = get_user_model()

class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Générer le token de vérification
            user.email_verification_token = str(uuid.uuid4())
            user.save()
            
            # Envoyer l'email de vérification avec Resend
            try:
                resend.api_key = settings.RESEND_API_KEY
                verification_url = f"{settings.FRONTEND_URL}/verify-email/{user.email_verification_token}"
                
                resend.Emails.send({
                    "from": "noreply@yourdomain.com",
                    "to": user.email,
                    "subject": "Vérifiez votre adresse email",
                    "html": f"""
                        <h1>Bienvenue sur notre plateforme!</h1>
                        <p>Merci de cliquer sur le lien ci-dessous pour vérifier votre adresse email:</p>
                        <a href="{verification_url}">Vérifier mon email</a>
                        <p>Ce lien expirera dans 24 heures.</p>
                    """
                })
                
                return Response({
                    "message": "Inscription réussie. Veuillez vérifier votre email."
                }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                user.delete()
                return Response({
                    "error": "Erreur lors de l'envoi de l'email de vérification"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def verify_email(self, request):
        token = request.data.get('token')
        if not token:
            return Response({
                "error": "Token manquant"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(
                email_verification_token=token,
                is_email_verified=False
            )
            
            # Vérifier si le token n'a pas expiré (24h)
            token_age = timezone.now() - user.date_joined
            if token_age.days >= 1:
                return Response({
                    "error": "Le lien de vérification a expiré"
                }, status=status.HTTP_400_BAD_REQUEST)
                
            user.is_email_verified = True
            user.email_verification_token = None
            user.save()
            
            return Response({
                "message": "Email vérifié avec succès"
            })
            
        except User.DoesNotExist:
            return Response({
                "error": "Token invalide"
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def resend_verification(self, request):
        email = request.data.get('email')
        if not email:
            return Response({
                "error": "Email manquant"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email, is_email_verified=False)
            
            # Générer un nouveau token
            user.email_verification_token = str(uuid.uuid4())
            user.save()
            
            # Renvoyer l'email
            resend.api_key = settings.RESEND_API_KEY
            verification_url = f"{settings.FRONTEND_URL}/verify-email/{user.email_verification_token}"
            
            resend.Emails.send({
                "from": "noreply@yourdomain.com",
                "to": user.email,
                "subject": "Vérifiez votre adresse email",
                "html": f"""
                    <h1>Nouveau lien de vérification</h1>
                    <p>Voici votre nouveau lien de vérification:</p>
                    <a href="{verification_url}">Vérifier mon email</a>
                    <p>Ce lien expirera dans 24 heures.</p>
                """
            })
            
            return Response({
                "message": "Email de vérification renvoyé"
            })
            
        except User.DoesNotExist:
            return Response({
                "error": "Utilisateur non trouvé ou déjà vérifié"
            }, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserDocumentViewSet(viewsets.ModelViewSet):
    """API endpoint pour gérer les documents des utilisateurs."""
    queryset = UserDocument.objects.all()
    serializer_class = UserDocumentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
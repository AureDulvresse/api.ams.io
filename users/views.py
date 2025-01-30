from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.forms import ValidationError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils import timezone
from users.serializers import (CustomTokenObtainPairSerializer, RegisterSerializer,
    UserDocumentSerializer, UserSerializer)
from users.models import UserDocument
import datetime
import uuid
import resend

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

    @action(detail=False, methods=['post'])
    def forgot_password(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            reset_token = str(uuid.uuid4())
            user.password_reset_token = reset_token
            user.password_reset_expires = timezone.now() + timezone.timedelta(hours=24)
            user.save()

            reset_url = f"{settings.FRONTEND_URL}/reset-password/{reset_token}"
            
            resend.api_key = settings.RESEND_API_KEY
            resend.Emails.send({
                "from": "noreply@yourdomain.com",
                "to": user.email,
                "subject": "Réinitialisation de votre mot de passe",
                "html": f"""
                    <h1>Réinitialisation de mot de passe</h1>
                    <p>Vous avez demandé une réinitialisation de votre mot de passe.</p>
                    <p>Cliquez sur le lien suivant pour créer un nouveau mot de passe:</p>
                    <a href="{reset_url}">Réinitialiser mon mot de passe</a>
                    <p>Ce lien expirera dans 24 heures.</p>
                    <p>Si vous n'êtes pas à l'origine de cette demande, ignorez cet email.</p>
                """
            })
            
            return Response({
                "message": "Instructions envoyées par email"
            })
            
        except User.DoesNotExist:
            # Même message pour éviter l'énumération des utilisateurs
            return Response({
                "message": "Instructions envoyées par email"
            })

    @action(detail=False, methods=['post'])
    def reset_password(self, request):
        token = request.data.get('token')
        password = request.data.get('password')
        
        try:
            user = User.objects.get(
                password_reset_token=token,
                password_reset_expires__gt=timezone.now()
            )
            
            user.set_password(password)
            user.password_reset_token = None
            user.password_reset_expires = None
            user.save()
            
            return Response({
                "message": "Mot de passe réinitialisé avec succès"
            })
            
        except User.DoesNotExist:
            return Response({
                "error": "Lien invalide ou expiré"
            }, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            if 'email' in serializer.validated_data:
                # Si l'email change, il faut le vérifier à nouveau
                new_email = serializer.validated_data['email']
                if new_email != user.email:
                    user.is_email_verified = False
                    user.email_verification_token = str(uuid.uuid4())
                    # Envoyer un nouvel email de vérification
                    self.send_verification_email(user, new_email)
            
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'])
    def change_password(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        
        if not user.check_password(current_password):
            return Response({
                "error": "Mot de passe actuel incorrect"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response({
                "error": e.messages
            }, status=status.HTTP_400_BAD_REQUEST)
            
        user.set_password(new_password)
        user.save()
        
        # Invalider les autres sessions
        TokenObtainPairView.objects.filter(user=user).delete()
        
        # Envoyer une notification
        self.send_security_notification(user)
        
        return Response({
            "message": "Mot de passe modifié avec succès"
        })

    @action(detail=False, methods=['put'])
    def update_notification_preferences(self, request):
        user = request.user
        preferences = request.data.get('preferences', {})
        
        user.notification_preferences.update(preferences)
        user.save()
        
        return Response(user.get_notification_settings())
class UserDocumentViewSet(viewsets.ModelViewSet):
    """API endpoint pour gérer les documents des utilisateurs."""
    queryset = UserDocument.objects.all()
    serializer_class = UserDocumentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
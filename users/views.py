from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
import jwt
import uuid
from users.email_service import EmailService
from .models import User, UserDocument
from .serializers import CustomTokenObtainPairSerializer, UserDocumentSerializer, UserSerializer

User = get_user_model()

class AuthViewSet(viewsets.GenericViewSet):
    """
    API endpoint pour gérer les utilisateurs.
    
    list:
    Retourne la liste de tous les utilisateurs.
    
    create:
    Crée un nouvel utilisateur.
    
    retrieve:
    Retourne les détails d'un utilisateur spécifique.
    
    update:
    Met à jour un utilisateur existant.
    
    partial_update:
    Met à jour partiellement un utilisateur existant.
    
    destroy:
    Supprime un utilisateur existant.
    """
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            verification_token = str(uuid.uuid4())
            user.email_verification_token = verification_token
            user.save()
            
            verification_url = f"{settings.FRONTEND_URL}/verify-email?token={verification_token}"
            
            try:
                EmailService.send_verification_email(user.email, verification_url)
                return Response(
                    {
                        "message": "Compte créé avec succès. Veuillez vérifier votre email pour activer votre compte.",
                        "user": serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                # En cas d'erreur d'envoi, on supprime l'utilisateur
                user.delete()
                return Response(
                    {"error": "Erreur lors de l'envoi de l'email de vérification."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def verify_email(self, request):
        token = request.query_params.get('token')
        try:
            user = User.objects.get(email_verification_token=token)
            if not user.is_email_verified:
                user.is_email_verified = True
                user.is_active = True
                user.email_verification_token = None  # Invalider le token après utilisation
                user.save()
                return Response({"message": "Email vérifié avec succès. Vous pouvez maintenant vous connecter."})
            return Response({"message": "Email déjà vérifié."})
        except User.DoesNotExist:
            return Response(
                {"error": "Token de vérification invalide"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    def resend_verification(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email, is_email_verified=False)
            
            # Génération d'un nouveau token
            verification_token = str(uuid.uuid4())
            user.email_verification_token = verification_token
            user.save()
            
            # Renvoi de l'email de vérification
            verification_url = f"{settings.FRONTEND_URL}/verify-email?token={verification_token}"
            send_mail(
                'Vérification de votre adresse email',
                f'Pour activer votre compte, veuillez cliquer sur ce lien: {verification_url}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            
            return Response({"message": "Email de vérification renvoyé avec succès."})
        except User.DoesNotExist:
            return Response(
                {"message": "Si l'email existe et n'est pas vérifié, un nouveau lien de vérification a été envoyé."},
                status=status.HTTP_200_OK
            )

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data)
        except Exception as e:
            user = User.objects.filter(email=request.data.get('email')).first()
            if user:
                user.failed_login_attempts += 1
                user.last_login_attempt = datetime.now()
                if user.failed_login_attempts >= 5:
                    user.is_blocked = True
                user.save()
            return Response(
                {"error": "Identifiants invalides"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    @action(detail=False, methods=['post'])
    def reset_password(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        
        if user:
            token = jwt.encode(
                {
                    'user_id': user.id,
                    'exp': datetime.utcnow() + timedelta(hours=24)
                },
                settings.SECRET_KEY,
                algorithm='HS256'
            )
            
            reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
            
            try:
                EmailService.send_password_reset_email(user.email, reset_url)
            except Exception as e:
                return Response(
                    {"error": "Erreur lors de l'envoi de l'email de réinitialisation."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
        return Response(
            {"message": "Si l'email existe, un lien de réinitialisation a été envoyé."},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['post'])
    def confirm_reset_password(self, request):
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            user.set_password(new_password)
            user.save()
            return Response({"message": "Mot de passe mis à jour avec succès"})
        except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
            return Response(
                {"error": "Lien invalide ou expiré"},
                status=status.HTTP_400_BAD_REQUEST
            )

class UserDocumentViewSet(viewsets.ModelViewSet):
    """API endpoint pour gérer les documents des utilisateurs."""
    queryset = UserDocument.objects.all()
    serializer_class = UserDocumentSerializer
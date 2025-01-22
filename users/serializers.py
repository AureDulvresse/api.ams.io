from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from django.utils import timezone
from .models import User, UserDocument
import re

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'role', 'phone', 
            'address', 'profile_photo', 'is_email_verified',
            'last_login', 'date_joined'
        )
        read_only_fields = (
            'is_email_verified', 'last_login', 
            'date_joined', 'failed_login_attempts'
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"validators": [EmailValidator()]},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Masquer les informations sensibles pour les non-admins
        user = self.context.get('request').user if self.context.get('request') else None
        if user and user.role != 'ADMIN':
            representation.pop('failed_login_attempts', None)
            representation.pop('last_login_ip', None)
        return representation

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True, 
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = (
            'email', 'username', 'password', 'password2', 
            'role', 'phone', 'address', 'profile_photo'
        )
        extra_kwargs = {
            'phone': {'required': False},
            'address': {'required': False},
            'profile_photo': {'required': False},
        }

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "Un utilisateur avec cette adresse email existe déjà."
            )
        return value.lower()

    # def validate_username(self, value):
    #     if User.objects.filter(username__iexact=value).exists():
    #         raise serializers.ValidationError(
    #             "Ce nom d'utilisateur est déjà pris."
    #         )
    #     if not re.match(r'^[\w.@+-]+$', value):
    #         raise serializers.ValidationError(
    #             "Le nom d'utilisateur ne peut contenir que des lettres, "
    #             "des chiffres et les caractères @/./+/-/_"
    #         )
    #     return value

    def validate_phone(self, value):
        if value:
            # Adaptation du regex selon votre format de numéro de téléphone
            if not re.match(r'^\+?1?\d{9,15}$', value):
                raise serializers.ValidationError(
                    "Format de numéro de téléphone invalide."
                )
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Les mots de passe ne correspondent pas"
            })
        
        # Validation du rôle
        if attrs.get('role') not in dict(User.Roles.choices):
            raise serializers.ValidationError({
                "role": "Rôle invalide"
            })
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Vérifier si l'utilisateur existe
        try:
            user = User.objects.get(email=attrs.get('email'))
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "email": "Aucun compte trouvé avec cette adresse email."
            })

        # Vérifier si le compte est bloqué
        if user.is_blocked:
            raise serializers.ValidationError({
                "detail": "Compte bloqué. Veuillez contacter l'administrateur."
            })

        # Vérifier le nombre de tentatives de connexion
        max_attempts = 5  # À définir selon vos besoins
        if user.failed_login_attempts >= max_attempts:
            user.is_blocked = True
            user.save()
            raise serializers.ValidationError({
                "detail": "Compte bloqué après trop de tentatives. "
                "Veuillez contacter l'administrateur."
            })

        try:
            data = super().validate(attrs)
        except serializers.ValidationError:
            # Incrémenter le compteur d'échecs
            user.failed_login_attempts += 1
            user.last_login_attempt = timezone.now()
            user.save()
            remaining_attempts = max_attempts - user.failed_login_attempts
            raise serializers.ValidationError({
                "detail": f"Mot de passe incorrect. "
                f"Il vous reste {remaining_attempts} tentative(s)."
            })

        if not self.user.is_email_verified:
            raise serializers.ValidationError({
                "detail": "Veuillez vérifier votre adresse email avant de vous connecter."
            })

        # Réinitialiser le compteur en cas de succès
        self.user.failed_login_attempts = 0
        self.user.last_login_ip = self.context['request'].META.get('REMOTE_ADDR')
        self.user.save()

        # Ajouter des informations supplémentaires au token
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'username': self.user.username,
            'role': self.user.role,
        }

        return data

class UserDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocument
        fields = '__all__'
        read_only_fields = ('user',)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate_file(self, value):
        # Limite de taille de fichier (5MB)
        max_size = 5 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError(
                "La taille du fichier ne doit pas dépasser 5MB."
            )
        
        # Validation des types de fichiers autorisés
        allowed_types = ['application/pdf', 'image/jpeg', 'image/png']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError(
                "Type de fichier non autorisé. "
                "Seuls les fichiers PDF, JPEG et PNG sont acceptés."
            )
        
        return value
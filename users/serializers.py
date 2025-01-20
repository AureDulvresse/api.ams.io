from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, UserDocument

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 
                 'role', 'phone', 'address', 'profile_photo']
        read_only_fields = ('id', 'is_email_verified')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            is_active=False  # Le compte sera activé après vérification
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        if not user.is_email_verified:
            raise serializers.ValidationError(
                "Veuillez vérifier votre adresse email avant de vous connecter."
            )

        if user.is_blocked:
            raise serializers.ValidationError(
                "Compte bloqué. Veuillez contacter l'administrateur."
            )

        user.failed_login_attempts = 0
        user.save()

        return data

class UserDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocument
        fields = '__all__'
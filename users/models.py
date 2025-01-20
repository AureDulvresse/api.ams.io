from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrateur système'
        DIRECTOR = 'DIRECTOR', 'Direction'
        DHR = 'DIRECTOR HR', 'Directeur RH'
        STAFF = 'STAFF', 'Personnel administratif'
        TEACHER = 'TEACHER', 'Enseignant'
        STUDENT = 'STUDENT', 'Étudiant'
        PARENT = 'PARENT', 'Parent'
        LIBRARIAN = 'LIBRARIAN', 'Bibliothécaire'
        ACCOUNTANT = 'ACCOUNTANT', 'Comptabilité'
        STOREKEEPER = 'STOREKEEPER', 'Magasinier'

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Roles.choices)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='profiles/', null=True, blank=True)
    failed_login_attempts = models.IntegerField(default=0)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_login_attempt = models.DateTimeField(null=True)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    is_blocked = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=255, null=True, blank=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class UserDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='Document'

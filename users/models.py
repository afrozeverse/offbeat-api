from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class Customer(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    role = models.CharField(
        max_length=20,
        choices=[
            ('user', 'User'),
            ('service_provider', 'Service Provider'),
            ('admin', 'Admin'),
        ],
        default='user'
    )

    is_verified = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email


class Provider(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # 🔥 FIX IS HERE
    user = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
        related_name='provider_profile'
    )

    display_name = models.CharField(max_length=100)
    about = models.CharField(max_length=300, null=True, blank=True)
    services_offered = models.JSONField(default=list)
    verified = models.BooleanField(default=False)
    contact_phone = models.CharField(max_length=15, null=True, blank=True)
    payout_info = models.CharField(max_length=100, blank=True, null=True)
    docs = models.ImageField(upload_to='provider_docs/', blank=True, null=True)

    def __str__(self):
        return self.display_name

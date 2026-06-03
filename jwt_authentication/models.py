from django.db import models
from django.contrib.auth.models import AbstractUser

import uuid
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    

class EmailVerificationToken(models.Model):

    user = models.OneToOneField(User, 
                                on_delete=models.CASCADE,
                                related_name="email_verfication_token"
                                )
    token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    

    def is_expired(self):
        expiry = getattr(settings, "EMAIL_VERIFICATION_EXPIRY_HOURS", 24)
    
        return timezone.now() > self.created_at + timedelta(hours=expiry)
    
    def __str__(self):
        return f"Verfication token for {self.user.email}"
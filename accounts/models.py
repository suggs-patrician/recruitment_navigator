from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
import string


class EmailVerificationCode(models.Model):
    """
    Model to store email verification codes for user registration
    """
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email} - {self.code}"

    def is_valid(self):
        """Check if the verification code is still valid"""
        return not self.is_used and self.expires_at > timezone.now()

    @classmethod
    def generate_code(cls, email, expiry_minutes=10):
        """
        Generate a new verification code for the given email
        If a code already exists for this email, update it
        """
        # Generate a random 6-digit code
        code = ''.join(random.choices(string.digits, k=6))
        
        # Calculate expiry time
        expires_at = timezone.now() + timezone.timedelta(minutes=expiry_minutes)
        
        # Create or update the verification code
        verification, created = cls.objects.update_or_create(
            email=email,
            defaults={
                'code': code,
                'expires_at': expires_at,
                'is_used': False
            }
        )
        
        return verification

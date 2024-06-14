from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import secrets

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('visitor', 'Visitor'),
        ('student', 'Student'),
        ('faculty', 'Faculty'),
    )

    VERIFICATION_STATUS_CHOICES = (
        ('not_verified', 'Not Verified'),
        ('verified', 'Verified'),
    )

    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default="visitor")
    first_name = models.CharField(max_length=20, default="...")
    last_name = models.CharField(max_length=20, default="...")
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS_CHOICES, default='not_verified')

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse('student_detail', kwargs={'pk': self.pk})

class VerificationID(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='verification_id')
    id_type = models.CharField(max_length=10, choices=[('student', 'Student'), ('faculty', 'Faculty')])
    id_value = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.id_type} ID: {self.id_value} for {self.user.username}"

class OtpToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="otps")
    otp_code = models.CharField(max_length=6, default=secrets.token_hex(3))
    otp_created_at = models.DateTimeField(auto_now_add=True)
    otp_expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    

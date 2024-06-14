from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from .models import OtpToken
from django.core.mail import send_mail
from django.utils import timezone
from django.core.exceptions import ValidationError

@receiver(post_save, sender=settings.AUTH_USER_MODEL) 
def create_token(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            pass
        else:
            try:
                # Create OTP token
                otp = OtpToken.objects.create(user=instance, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
                
                # Send verification email
                send_verification_email(instance, otp)
            except Exception as e:
                # Handle email sending error
                print(f"Failed to send verification email to {instance.email}: {str(e)}")
                # Delete the user if email sending fails
                instance.delete()

def send_verification_email(user, otp):
    subject = "Email Verification"
    message = f"""
        Hi {user.username}, here is your OTP: {otp.otp_code}.
        It expires in 5 minutes. Please use the following link to verify your email address:
        http://127.0.0.1:8000/verify-email/{user.username}
    """
    sender_email = "manage125business@gmail.com"
    receiver_email = [user.email]

    try:
        send_mail(
            subject,
            message,
            sender_email,
            receiver_email,
            fail_silently=False,
        )
    except Exception as e:
        # Raise an exception if email sending fails
        raise ValidationError(f"Failed to send verification email: {str(e)}")

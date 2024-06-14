from django.db import models
from manage_users.models import CustomUser
# Create your models here.

class Notification(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_notifications')
    recipients = models.ManyToManyField(CustomUser, related_name='received_notifications')

    def __str__(self):
        return self.message
    
class PersonalInfoFaculty(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    phone_number = models.CharField(max_length=20)
    address = models.TextField(max_length=500)
    aadhar_front = models.ImageField(upload_to='', null=True, blank=True)
    aadhar_back = models.ImageField(upload_to='', null=True, blank=True)
    profile_picture = models.ImageField(upload_to='', null=True, blank=True)

    def __str__(self):
        return f"PersonalInfo for {self.user.username}"

class SkillsFaculty(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=100)
    proficiency_level = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    skill_certificate = models.ImageField(upload_to='skill_certificates/', null=True, blank=True)
    
class AchievementsFaculty(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    achievement_title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    achievement_certificate = models.ImageField(upload_to='achievement_certificates/', null=True, blank=True)

class InterestsFaculty(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    interest = models.CharField(max_length=100)
    interest_certificate = models.ImageField(upload_to='interest_certificates/', null=True, blank=True)

class LanguagesFaculty(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    language = models.CharField(max_length=100)
    proficiency_level = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    language_certificate = models.ImageField(upload_to='language_certificates/', null=True, blank=True)

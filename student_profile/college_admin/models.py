from django.urls import reverse
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from phonenumber_field.modelfields import PhoneNumberField
from manage_users.models import CustomUser

# Create your models here.
class AdminUser(AbstractUser):
    email = models.EmailField(unique=True)
    adminID = models.IntegerField(unique=True)

    groups = models.ManyToManyField(Group, related_name='admin_users')
    user_permissions = models.ManyToManyField(Permission, related_name='admin_users_permissions')

    REQUIRED_FIELDS = ["adminID"]
    def __str__(self):
        return self.username


class Course(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=50)
    syllabus_files = models.FileField(upload_to='syllabus/', default="syllabus/default.pdf")
    duration = models.DurationField(default="...")
    eligibility_criteria = models.TextField(default="...")
    instructors = models.ManyToManyField(CustomUser, limit_choices_to={'user_type': 'faculty'})

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('course_detail', args=[str(self.id)])
    
    @staticmethod
    def verified_students_count():
        return CustomUser.objects.filter(user_type='student', verification_status='verified').count()
    
    @staticmethod
    def not_verified_students_count():
        return CustomUser.objects.filter(user_type='student', verification_status='not_verified').count()
    
    @staticmethod
    def not_verified_students():
        return CustomUser.objects.filter(user_type='student', verification_status='not_verified')

    @staticmethod
    def enrolled_students_count():
        return Student.objects.filter(enrollment_status='enrolled').count()

    @staticmethod
    def faculty_count():
        return CustomUser.objects.filter(user_type='faculty').count()

class Specialization(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default="...")
    course = models.ForeignKey(Course, related_name='specializations', on_delete=models.CASCADE, default="...")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('specialization_detail', args=[str(self.id)])
    
class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    courses = models.ManyToManyField(Course, blank=True)
    specializations = models.ManyToManyField(Specialization, blank=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username if self.recipient else 'multiple recipients'}"
    
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'student'})
    courses = models.ManyToManyField(Course, blank=True)
    specializations = models.ManyToManyField(Specialization, blank=True)
    personal_info = models.ManyToManyField('manage_students.PersonalInfo', blank=True)
    enrollment_date = models.DateField(auto_now_add=True)
    enrollment_status = models.CharField(max_length=50, default="...", choices=[
        ('enrolled', 'Enrolled'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped')
    ])

    def __str__(self):
        return self.user.username

class HiredStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    hire_date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True)
    employer_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    department = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.student.user.username
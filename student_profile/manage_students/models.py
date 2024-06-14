from django.utils import timezone
from django.db import models
from manage_users.models import CustomUser
from college_admin.models import Course, Specialization

class PersonalInfo(models.Model):
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

class CollegeInfo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=20)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.roll_no} - {self.course.name} - {self.specialization.name if self.specialization else 'No Specialization'}"

    def save(self, *args, **kwargs):
        # Call the superclass method to perform the actual save operation
        super().save(*args, **kwargs)

        # Check if the associated student exists
        if hasattr(self, 'student'):
            student = self.student
            student.courses.add(self.course)  # Add the course to the student's courses
            student.specializations.add(self.specialization)  # Add the specialization to the student's specializations

        # Check if the associated enrollment exists
        if hasattr(self, 'enrollment'):
            enrollment = self.enrollment
            enrollment.course = self.course  # Update the course in the enrollment
            enrollment.specializations.set([self.specialization])  # Update the specialization in the enrollment
            enrollment.save()  # Save the updated enrollment

class EducationInfo(models.Model):
    YEAR_CHOICES = [(year, str(year)) for year in range(1970, 2031)]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tenth_school = models.CharField(max_length=100)
    tenth_year = models.IntegerField(choices=YEAR_CHOICES)
    tenth_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    tenth_school_certificate = models.ImageField(upload_to='', null=True, blank=True)
    twelfth_school = models.CharField(max_length=100)
    twelfth_year = models.IntegerField(choices=YEAR_CHOICES)
    twelfth_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    twelfth_school_certificate = models.ImageField(upload_to='', null=True, blank=True)
    degree_college = models.CharField(max_length=100)
    degree_course = models.CharField(max_length=100)
    degree_year = models.IntegerField(choices=YEAR_CHOICES)
    degree_certificate = models.ImageField(upload_to='', null=True, blank=True)

    def __str__(self):
        return f"EducationInfo for {self.user.username}"
        
class Document(models.Model):
    DOCUMENT_TYPES = [
        ('resume', 'Resume'),
        # Add more document types as needed
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    document_file = models.FileField(upload_to='')

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.user.username}"

class Experience(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    certificate = models.ImageField(upload_to='', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Experience: {self.job_title}"

class Project(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    project_document = models.FileField(upload_to='project_documents/', null=True, blank=True)
    project_links = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Project: {self.project_name}"

class Skills(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=100)
    proficiency_level = models.IntegerField(choices=[(i, i) for i in range(1, 11)])  # Choices from 1 to 10
    skill_certificate = models.ImageField(upload_to='skill_certificates/', null=True, blank=True)
    
class Achievements(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    achievement_title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    achievement_certificate = models.ImageField(upload_to='achievement_certificates/', null=True, blank=True)

class Interests(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    interest = models.CharField(max_length=100)
    interest_certificate = models.ImageField(upload_to='interest_certificates/', null=True, blank=True)

class Languages(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    language = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=50)
    language_certificate = models.ImageField(upload_to='language_certificates/', null=True, blank=True)

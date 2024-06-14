from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.urls import reverse_lazy

from college_admin.models import Course, Specialization, Student
from manage_students.models import Course, Document, PersonalInfo, CollegeInfo, EducationInfo, Skills, Experience, Project, Achievements, Interests, Languages

from .forms import EmailForm, RegisterForm, RegisterFormFaculty, RegisterFormStudent
from django.contrib import messages
from .models import CustomUser
from django.core.mail import send_mail
from django.utils import timezone
from .models import OtpToken

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data

            # Extract and handle password separately
            password = user_data.pop('password1')
            user_data.pop('password2')

            # Create a user instance
            user_model = get_user_model()
            user = user_model(**user_data)
            user.set_password(password)
            user.is_active = False  # Initially inactive
            user.save()

            # Generate OTP and save it
            otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))

            # Send email
            subject = "Email Verification"
            message = f"Hi {user.username}, here is your OTP {otp.otp_code}. It expires in 5 minutes. Use the URL below to verify your email: http://127.0.0.1:5000/manage_users/verify-email/{user.username}"
            sender = "your-email@gmail.com"
            receiver = [user.email]

            try:
                send_mail(subject, message, sender, receiver, fail_silently=False)
                messages.success(request, "An OTP was sent to your email for verification.")
            except Exception as e:
                print(f"Error sending email: {e}")
                messages.error(request, "Error sending email. Please try again.")

            return redirect("verify-email", username=user.username)
    else:
        form = RegisterForm()
    context = {"form": form}
    return render(request, "main/signup.html", context)

def signup_student(request):
    if request.method == 'POST':
        form = RegisterFormStudent(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data
            
            # Extract and handle fields separately
            password = user_data.pop('password1')
            user_data.pop('password2')
            student_id = user_data.pop('student_id')

            # Add additional user type field
            user_data['user_type'] = 'student'
            
            # Create a user instance
            user_model = get_user_model()
            user = user_model(**user_data)
            user.set_password(password)
            user.is_active = False  # Initially inactive
            user.save()

            # Save the student ID or other additional fields if necessary
            # Assuming there is a StudentProfile model related to the user
            # StudentProfile.objects.create(user=user, student_id=student_id)

            # Generate OTP and save it
            otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))

            # Send email
            subject = "Email Verification"
            message = f"Hi {user.username}, here is your OTP {otp.otp_code}. It expires in 5 minutes. Use the URL below to verify your email: http://127.0.0.1:5000/manage_users/verify-email/{user.username}"
            sender = "your-email@gmail.com"
            receiver = [user.email]

            try:
                send_mail(subject, message, sender, receiver, fail_silently=False)
                messages.success(request, "An OTP was sent to your email for verification.")
            except Exception as e:
                print(f"Error sending email: {e}")
                messages.error(request, "Error sending email. Please try again.")

            return redirect("verify-email", username=user.username)
    else:
        form = RegisterFormStudent()
    context = {"form": form}
    return render(request, "main/signup.html", context)

def signup_faculty(request):
    if request.method == 'POST':
        form = RegisterFormFaculty(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data

            # Extract and handle fields separately
            password = user_data.pop('password1')
            user_data.pop('password2')
            faculty_id = user_data.pop('faculty_id')

            # Add additional user type field
            user_data['user_type'] = 'faculty'
            
            # Create a user instance
            user_model = get_user_model()
            user = user_model(**user_data)
            user.set_password(password)
            user.is_active = False  # Initially inactive
            user.save()

            # Save the faculty ID or other additional fields if necessary
            # Assuming there is a FacultyProfile model related to the user
            # FacultyProfile.objects.create(user=user, faculty_id=faculty_id)

            # Generate OTP and save it
            otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))

            # Send email
            subject = "Email Verification"
            message = f"Hi {user.username}, here is your OTP {otp.otp_code}. It expires in 5 minutes. Use the URL below to verify your email: http://127.0.0.1:5000/manage_users/verify-email/{user.username}"
            sender = "your-email@gmail.com"
            receiver = [user.email]

            try:
                send_mail(subject, message, sender, receiver, fail_silently=False)
                messages.success(request, "An OTP was sent to your email for verification.")
            except Exception as e:
                print(f"Error sending email: {e}")
                messages.error(request, "Error sending email. Please try again.")

            return redirect("verify-email", username=user.username)
    else:
        form = RegisterFormFaculty()
    context = {"form": form}
    return render(request, "main/signup.html", context)

def verify_email(request, username):
    user_model = get_user_model()
    
    try:
        user = user_model.objects.get(username=username)
    except user_model.DoesNotExist:
        messages.error(request, "User does not exist.")
        return redirect("signup")

    user_otp = OtpToken.objects.filter(user=user).last()

    if request.method == 'POST':
        if user_otp and user_otp.otp_code == request.POST['otp_code']:
            if user_otp.otp_expires_at > timezone.now():
                user.is_active = True  # Activate the user
                user.save()

                messages.success(request, "Account activated successfully! You can log in.")
                return redirect("signin")
            else:
                messages.warning(request, "The OTP has expired, get a new OTP!")
                return redirect("resend-otp")
        else:
            messages.warning(request, "Invalid OTP entered, enter a valid OTP!")
            return redirect("verify-email", username=user.username)

    context = {"username": username}
    return render(request, "main/verify.html", context)

def resend_otp(request):
    user_data = request.session.get('user_data')
    if not user_data:
        messages.error(request, "Session expired or invalid. Please sign up again.")
        return redirect("signup")

    if request.method == 'POST':
        user_email = user_data.get('email')
        
        if user_email:
            user_model = get_user_model()
            user = user_model(**user_data)  # Create a user instance but don't save it to the database
            otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))

            # email variables
            subject = "Email Verification"
            message = f"Hi {user.username}, here is your OTP {otp.otp_code}. It expires in 5 minutes. Use the URL below to verify your email: http://127.0.0.1:8000/verify-email/"
            sender = "your-email@example.com"
            receiver = [user.email]

            # send email
            send_mail(subject, message, sender, receiver, fail_silently=False)

            messages.success(request, "A new OTP has been sent to your email address.")
            return redirect("verify-email")
        else:
            messages.warning(request, "Email address not found.")
            return redirect("resend-otp")

    return render(request, "main/resend_otp.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return render(request, "adminindex.html")
            elif user.user_type == 'faculty':
                return render(request, "facultyindex.html")
            elif user.user_type == 'student':
                return render(request, "studentindex.html")
            else:
                return render(request, "index.html")
            
        else:
            messages.warning(request, "Invalid credentials")
            return redirect("signin")
        
    return render(request, "main/login.html")

def handle_logout(request):
    logout(request)
    request.session.flush()
    messages.success(request, "Successfully Logged Out")
    return redirect('index')

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'main/reset_pass.html'
    email_template_name = 'main/reset_pass_email.html'
    subject_template_name = 'main/reset_pass_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('signin')

#  Navbar Views
def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "main/about.html")

def courses(request):
    return render(request, "main/courses.html")

def contact(request):
    return render(request, "main/contact.html")

def iqac(request):
    return render(request, "main/iqac.html")

def team(request):
    return render(request, "main/team.html")

def profile(request):
    return render(request, 'student_profile.html')

def recruitment(request):
    courses = Course.objects.all()
    
    return render(request, 'main/recruitment.html', {
        'courses': courses,
    })

# Student Profile Views

def student_details(request, username):
    student = get_object_or_404(CustomUser, username=username)
    personal_info = get_object_or_404(PersonalInfo, user=student)
    college_info = CollegeInfo.objects.filter(user=student)
    education_info = EducationInfo.objects.filter(user=student)
    documents = Document.objects.filter(user=student)
    experiences = Experience.objects.filter(user=student)
    projects = Project.objects.filter(user=student)
    skills = Skills.objects.filter(user=student)
    achievements = Achievements.objects.filter(user=student)
    interests = Interests.objects.filter(user=student)
    languages = Languages.objects.filter(user=student)
    
    if request.method == 'POST':
        # Assuming you have a form to send email
        form = EmailForm(request.POST)
        if form.is_valid():
            sender_email = request.user.email
            recipient_email = student.email
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            send_mail(subject, message, sender_email, [recipient_email])
            # Optionally, add a success message or redirect to another page
            return HttpResponseRedirect('/success/')
    else:
        form = EmailForm()  # Assuming you have a form to send email
    
    context = {
        'student': student,
        'personal_info': personal_info,
        'college_info': college_info,
        'education_info': education_info,
        'documents': documents,
        'experiences': experiences,
        'projects': projects,
        'skills': skills,
        'achievements': achievements,
        'interests': interests,
        'languages': languages,
        'form': form,  # Pass the form to the template context
    }
    
    return render(request, 'student_profile.html', context)

class CourseDetailView(DetailView):
    model = Course
    template_name = 'course_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = Student.objects.filter(courses=self.object)
        context['courses'] = Course.objects.all()
        context['personal_info'] = PersonalInfo.objects.filter(profile_picture=self.object)
        return context\

class SpecializationDetailView(DetailView):
    model = Specialization
    template_name = 'specialization_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filter students by the current specialization
        context['students'] = Student.objects.filter(specializations=self.object)
        context['courses'] = Course.objects.all()
        return context
    
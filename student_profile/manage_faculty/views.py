import json
from django.http import JsonResponse
from django.shortcuts import redirect, render

from manage_users.models import CustomUser, VerificationID
from manage_students.models import Document, Experience, Project, Skills, Achievements, Interests, Languages
from college_admin.models import Course

from .models import PersonalInfoFaculty, SkillsFaculty, InterestsFaculty, AchievementsFaculty, LanguagesFaculty
from .forms import NotificationForm, PersonalInfoForm, SkillsForm, AchievementsForm, InterestsForm, LanguagesForm
from django.apps import apps
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def send_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.sender = request.user
            notification.save()
            form.save_m2m()  # Save the many-to-many relationship
            return redirect('view_notification')
    else:
        form = NotificationForm()
    return render(request, 'send_notification.html', {'form': form})

def view_notification(request):
    return render(request, "send_notification.html")

def form_view_faculty(request, tab):
    total_tabs = 5  # Assuming you have 5 tabs

    next_tabs = {
        'personal': 'skills',
        'skills': 'achievements',
        'achievements': 'interests',
        'interests': 'languages',
        'languages': 'personal'  # Loop back to the first tab
    }

    form_classes = {
        'personal': PersonalInfoForm,
        'skills': SkillsForm,
        'achievements': AchievementsForm,
        'interests': InterestsForm,
        'languages': LanguagesForm,
    }

    current_form_class = form_classes.get(tab)

    if request.method == 'POST':
        current_form = current_form_class(request.POST, request.FILES)
        if current_form.is_valid():
            form_instance = current_form.save(commit=False)
            form_instance.user = request.user
            form_instance.user_id = request.user.id
            form_instance.save()

            next_tab = next_tabs.get(tab, 'personal')
            return redirect('form_view_faculty', tab=next_tab)
    else:
        edit_instance_id = request.GET.get('edit_instance_id')
        if edit_instance_id:
            model_class_name, _ = next(filter(lambda x: x[0] == tab, form_classes.items()))
            model_class = apps.get_model('manage_faculty', model_class_name)
            instance = get_object_or_404(model_class, id=edit_instance_id, user=request.user)
            current_form = current_form_class(instance=instance)
        else:
            current_form = current_form_class()

    progress = (list(next_tabs.keys()).index(tab) + 1) / total_tabs * 100

    is_editing = request.GET.get('edit', False)

    personal_info = PersonalInfoFaculty.objects.filter(user=request.user).first()
    skills = SkillsFaculty.objects.filter(user=request.user)
    achievements = AchievementsFaculty.objects.filter(user=request.user)
    interests = InterestsFaculty.objects.filter(user=request.user)
    languages = LanguagesFaculty.objects.filter(user=request.user)

    return render(request, 'editprofilefaculty.html', {
        'current_form': current_form,
        'active_tab': tab,
        'progress': progress,
        'personal_info': personal_info,
        'skills': skills,
        'achievements': achievements,
        'interests': interests,
        'languages': languages,
        'is_editing': is_editing,
        'next_tab': next_tabs.get(tab, 'personal'),
        'proficiency_levels': range(1, 11)
    })

@csrf_exempt
def verify_faculty_id(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        faculty_id = data.get('facultyID')
        
        try:
            verification_id = VerificationID.objects.get(id_value=faculty_id, id_type='faculty')
            if verification_id.user == request.user:
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid Faculty ID for this user'})
        except VerificationID.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid Faculty ID'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def dashboard_home_faculty(request):
    try:
        personal_info = PersonalInfoFaculty.objects.get(user=request.user)
    except PersonalInfoFaculty.DoesNotExist:
        personal_info = None

    total_fields = 5  # Update this if you have more fields
    filled_fields = 0

    if PersonalInfoFaculty.objects.filter(user=request.user).exists():
        filled_fields += 1

    if SkillsFaculty.objects.filter(user=request.user).exists():
        filled_fields += 1

    if AchievementsFaculty.objects.filter(user=request.user).exists():
        filled_fields += 1

    if InterestsFaculty.objects.filter(user=request.user).exists():
        filled_fields += 1

    if LanguagesFaculty.objects.filter(user=request.user).exists():
        filled_fields += 1

    completion_percentage = (filled_fields / total_fields) * 100

    return render(request, 'facultydashboard.html', {'personal_info': personal_info, 'completion_percentage': completion_percentage})

@require_POST
def delete_personal_info(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        print("User ID:", user_id)
        # Use user_id to delete the user's personal information from the database
        PersonalInfoFaculty.objects.filter(user_id=user_id).delete()
        # Redirect to the page where the form is displayed
        return redirect('form_view_faculty', tab='personal') 

def delete_instance(request, active_tab, instance_id):
    # Determine the model class based on the active_tab
    model_classes = {
        'personal': PersonalInfoFaculty,
        'skills': SkillsFaculty,
        'achievements': AchievementsFaculty,
        'interests': InterestsFaculty,
        'languages': LanguagesFaculty,
    }
    model_class = model_classes.get(active_tab)
    
    # Get the instance to delete
    instance = get_object_or_404(model_class, id=instance_id)
    
    # Delete the instance
    instance.delete()
    
    # Add a success message
    messages.success(request, f'{model_class._meta.verbose_name} deleted successfully.')
    
    # Redirect back to the form view for the same tab
    return redirect('form_view_faculty', tab=active_tab)

def facultyindex(request):
    return render(request, 'facultyindex.html')

def verify_students(request):
    students = CustomUser.objects.filter(user_type="student")
    context = {"students": students}
    return render(request, "verify_students.html", context)

def student_detail(request, pk):
    student = get_object_or_404(CustomUser, pk=pk)
    documents = Document.objects.filter(user=student)
    experiences = Experience.objects.filter(user=student)
    projects = Project.objects.filter(user=student)
    skills = Skills.objects.filter(user=student)
    achievements = Achievements.objects.filter(user=student)
    interests = Interests.objects.filter(user=student)
    languages = Languages.objects.filter(user=student)

    context = {
        "student": student,
        "documents": documents,
        "experiences": experiences,
        "projects": projects,
        "skills": skills,
        "achievements": achievements,
        "interests": interests,
        "languages": languages,
    }

    return render(request, "student_detail.html", context)

# main Pages
def recruitmentF(request):
    courses = Course.objects.all()
    return render(request, "mainF/recruitmentF.html", {courses : 'courses'})

def aboutF(request):
    return render(request, "mainF/aboutF.html")

def coursesF(request):
    return render(request, "mainF/coursesF.html")

def contactF(request):
    return render(request, "mainF/contactF.html")

def iqacF(request):
    return render(request, "mainF/iqacF.html")

def teamF(request):
    return render(request, "mainF/teamF.html")

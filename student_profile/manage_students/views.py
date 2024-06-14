import json
from django.apps import apps
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from django.apps import apps
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from manage_faculty.models import Notification
from college_admin.models import Course, Message, Specialization
from manage_users.models import CustomUser, VerificationID
from .forms import AchievementsForm, CollegeInfoForm, InterestsForm, LanguagesForm, PersonalInfoForm, EducationInfoForm, DocumentForm, ExperienceForm, ProjectForm, SkillsForm
from .models import Achievements, CollegeInfo, Interests, Languages, PersonalInfo, EducationInfo, Document, Experience, Project, Skills
from django.views.decorators.http import require_POST

def view_notifications(request):
    notifications = Notification.objects.filter(recipients=request.user)
    return render(request, 'notifications.html', {'notifications': notifications})

@login_required
def form_view(request, tab):
    total_tabs = 10  # Assuming you have 5 tabs

    next_tabs = {
        'personal': 'education',
        'education': 'college_info',
        'college_info': 'document',
        'document': 'experience',
        'experience': 'project',
        'project': 'skills',
        'skills': 'achievements',
        'achievements': 'interests',
        'interests': 'languages',
        'languages': 'personal'  # Loop back to the first tab
    }

    form_classes = {
        'personal': PersonalInfoForm,
        'education': EducationInfoForm,
        'college_info': CollegeInfoForm,
        'document': DocumentForm,
        'experience': ExperienceForm,
        'project': ProjectForm,
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
            return redirect('form_view', tab=next_tab)
    else:
        edit_instance_id = request.GET.get('edit_instance_id')
        if edit_instance_id:
            # Adjust the model class name here
            model_class_name = tab.capitalize()  # Assuming tab name matches model name
            model_class = apps.get_model('manage_students', model_class_name)
            instance = get_object_or_404(model_class, id=edit_instance_id, user=request.user)
            current_form = current_form_class(instance=instance)
        else:
            current_form = current_form_class()

    progress = (list(next_tabs.keys()).index(tab) + 1) / total_tabs * 100

    # Fetch other related data like education, document, etc.
    education_info = EducationInfo.objects.filter(user=request.user)
    college_info = CollegeInfo.objects.filter(user=request.user)
    document = Document.objects.filter(user=request.user)
    experience = Experience.objects.filter(user=request.user)
    project = Project.objects.filter(user=request.user)
    skills = Skills.objects.filter(user=request.user)
    achievements = Achievements.objects.filter(user=request.user)
    interests = Interests.objects.filter(user=request.user)
    languages = Languages.objects.filter(user=request.user)

    is_editing = request.GET.get('edit', False)

    personal_info = PersonalInfo.objects.filter(user=request.user).first()

    return render(request, 'editprofile.html', {
        'current_form': current_form,
        'active_tab': tab,
        'progress': progress,
        'personal_info': personal_info,
        'education_info': education_info,
        'college_info': college_info,
        'document': document,
        'experience': experience,
        'project': project,
        'skills': skills,
        'achievements': achievements,
        'interests': interests,
        'languages': languages,
        'is_editing': is_editing,
        'next_tab': next_tabs.get(tab, 'personal'),
        'proficiency_levels': range(1, 11)
    })

@require_POST
def delete_personal_info(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        print("User ID:", user_id)
        # Use user_id to delete the user's personal information from the database
        PersonalInfo.objects.filter(user_id=user_id).delete()
        # Redirect to the page where the form is displayed
        return redirect('form_view', tab='personal')
    
@login_required
def delete_education_info(request):
    if request.method == 'POST':
        info_id = request.POST.get('info_id')
        # Ensure the user is an admin before deleting
        if request.user.is_authenticated:
            # Fetch the education info object to delete
            info_to_delete = get_object_or_404(EducationInfo, id=info_id)
            # Delete the object
            info_to_delete.delete()
    return redirect('form_view', tab='education') 

def delete_instance(request, active_tab, instance_id):
    # Determine the model class based on the active_tab
    model_classes = {
        'experience': Experience,  # Assuming 'experience' is the tab name for the Experience model
        'personal_info': PersonalInfo,
        'education': EducationInfo,
        'document': Document,
        'project': Project
    }
    model_class = model_classes.get(active_tab)
    
    # Get the instance to delete
    instance = get_object_or_404(model_class, id=instance_id)
    
    # Delete the instance
    instance.delete()
    
    # Add a success message
    messages.success(request, f'{model_class._meta.verbose_name} deleted successfully.')
    
    # Redirect back to the form view for the same tab
    return redirect('form_view', tab=active_tab)

@csrf_exempt
def verify_student_id(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        student_id = data.get('studentID')
        
        try:
            verification_id = VerificationID.objects.get(id_value=student_id, id_type='student')
            if verification_id.user == request.user:
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid Student ID for this user'})
        except VerificationID.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid Student ID'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def dashboard_home(request):
    try:
        personal_info = PersonalInfo.objects.get(user=request.user)
    except PersonalInfo.DoesNotExist:
        personal_info = None
    
    total_fields = 9  # Update this if you have more fields
    filled_fields = 0

    if hasattr(request.user, 'personalinfo'):
        filled_fields += 1

    if EducationInfo.objects.filter(user=request.user).exists():
        filled_fields += 1

    if Experience.objects.filter(user=request.user).exists():
        filled_fields += 1

    if Project.objects.filter(user=request.user).exists():
        filled_fields += 1

    if Skills.objects.filter(user=request.user).exists():
        filled_fields += 1

    if Achievements.objects.filter(user=request.user).exists():
        filled_fields += 1

    if Interests.objects.filter(user=request.user).exists():
        filled_fields += 1

    if Languages.objects.filter(user=request.user).exists():
        filled_fields += 1

    completion_percentage = (filled_fields / total_fields) * 100

    try:
        latest_notification = Notification.objects.filter(recipients=request.user).latest('timestamp')
    except Notification.DoesNotExist:
        latest_notification = None

    current_student = request.user

    try:
        message = Message.objects.filter(recipient=current_student)
    except message.DoesNotExist:
        message = None

    try:
        student = CustomUser.objects.get(user_type='student')
        verify_status = student.verification_status
    except CustomUser.DoesNotExist:
        verify_status = None

    context = {'verify_status': verify_status, 'message': message, 'personal_info': personal_info, 'completion_percentage': completion_percentage, 'latest_notification': latest_notification}
    return render(request, 'studentdashboard.html', context )


def studentindex(request):
    return render(request, 'studentindex.html')

def view_profile(request):
    return render(request, 'viewprofile.html')


# Main Pages
def recruitmentS(request):
    courses = Course.objects.all()
    return render(request, "mainF/recruitmentS.html", {courses : 'courses'})

def aboutS(request):
    return render(request, "main/aboutS.html")

def coursesS(request):
    return render(request, "main/coursesS.html")

def contactS(request):
    return render(request, "main/contactS.html")

def iqacS(request):
    return render(request, "main/iqacS.html")

def teamS(request):
    return render(request, "main/teamS.html")

def profileS(request):
    return render(request, 'student_profile.html')

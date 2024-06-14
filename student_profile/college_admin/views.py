from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.shortcuts import render
from manage_students.models import PersonalInfo, CollegeInfo, EducationInfo, Document, Experience, Project, Skills, Achievements, Interests, Languages
from manage_users.models import CustomUser
from manage_faculty.models import PersonalInfoFaculty, AchievementsFaculty, InterestsFaculty, LanguagesFaculty, SkillsFaculty
from college_admin.models import Course, HiredStudent, Message, Specialization, Student
from college_admin import models
from .forms import MessageForm
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator

# Create your views here.
@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            recipients = form.get_filtered_recipients()
            message.recipients.set(recipients)
            return redirect('message_sent')  # Redirect to a 'message sent' page
    else:
        form = MessageForm()

    return render(request, 'notice.html', {'form': form})

def adminindex(request):
    return render(request, "adminindex.html")

def admin_dash(request):

    messages = Message.objects.filter(sender=request.user).order_by('-sent_at')
    paginator = Paginator(messages, 5)  # Show 5 messages per page
    page_number = request.GET.get('page')
    sent_messages = paginator.get_page(page_number)

    not_verified_users = CustomUser.objects.filter(user_type='student', verification_status='not_verified')
    not_verified_students = Student.objects.filter(user__in=not_verified_users)

    enrolled_students_count = Student.objects.filter(enrollment_status='enrolled').count()
    completed_students_count = Student.objects.filter(enrollment_status='completed').count()
    dropped_students_count = Student.objects.filter(enrollment_status='dropped').count()

    verified_students_count = CustomUser.objects.filter(verification_status='verified').count()
    not_verified_students_count = CustomUser.objects.filter(verification_status='not_verified').count()

    # Combining data
    statuses = ['Enrolled', 'Completed', 'Dropped', 'Verified', 'Not Verified']
    counts = [enrolled_students_count, completed_students_count, dropped_students_count,
              verified_students_count, not_verified_students_count]

    context = {
        'verified_students': Course.verified_students_count(),
        'not_verified_students_count': Course.not_verified_students_count(),
        'not_verified_students': not_verified_students,
        'enrolled_students': Course.enrolled_students_count(),
        'faculties': Course.faculty_count(),
        'sent_messages': sent_messages,
        'statuses': statuses,
        'counts': counts,
    }

    # Fetch data for the enrollment chart
    students = Student.objects.all()
    statuses = students.values('enrollment_status').annotate(count=Count('enrollment_status'))
    context['enrollment_statuses'] = [status['enrollment_status'] for status in statuses]
    context['enrollment_counts'] = [status['count'] for status in statuses]

    return render(request, 'admin_dashboard.html', context)

def enrollment_chart_data(request):
    students = Student.objects.all()
    statuses = students.values('enrollment_status').annotate(count=models.Count('enrollment_status'))
    data = {
        'statuses': [status['enrollment_status'] for status in statuses],
        'counts': [status['count'] for status in statuses]
    }
    return JsonResponse(data)

def analysis(request):

    enrolled_students_count = Student.objects.filter(enrollment_status='enrolled').count()
    completed_students_count = Student.objects.filter(enrollment_status='completed').count()
    dropped_students_count = Student.objects.filter(enrollment_status='dropped').count()

    verified_students_count = CustomUser.objects.filter(verification_status='verified').count()
    not_verified_students_count = CustomUser.objects.filter(verification_status='not_verified').count()

    # Combining data
    statuses = ['Enrolled', 'Completed', 'Dropped', 'Verified', 'Not Verified']
    counts = [enrolled_students_count, completed_students_count, dropped_students_count,
              verified_students_count, not_verified_students_count]
    
    context = {
        'verified_students': Course.verified_students_count(),
        'enrolled_students': Course.enrolled_students_count(),
        'faculties': Course.faculty_count(),
        'statuses': statuses,
        'counts': counts,
    }

    # Fetch data for the enrollment chart
    students = Student.objects.all()
    statuses = students.values('enrollment_status').annotate(count=Count('enrollment_status'))
    context['enrollment_statuses'] = [status['enrollment_status'] for status in statuses]
    context['enrollment_counts'] = [status['count'] for status in statuses]

    return render(request, 'analysis.html', context)

def hired_students_view(request):
    course_id = request.GET.get('course')
    hired_students = HiredStudent.objects.select_related('student__user', 'course').all()

    if course_id:
        hired_students = hired_students.filter(course_id=course_id)

    filter_programs = Course.objects.all()

    context = {
        'hired_students': hired_students,
        'filter_programs': filter_programs,
    }
    return render(request, 'hired_student.html', context)

def verify_faculty(request):
    faculty = CustomUser.objects.filter(user_type="faculty")
    context = {"faculty": faculty}
    return render(request, "verify_faculty.html", context)

def verify_students_admin(request):
    students = CustomUser.objects.filter(user_type="student")
    context = {"students": students}
    return render(request, "verify_students_admin.html", context)

def student_detail_admin(request, pk):
    student = get_object_or_404(CustomUser, pk=pk)

    try:
        personal_info = PersonalInfo.objects.get(user=student)
    except PersonalInfo.DoesNotExist:
        personal_info = None

    try:
        college_info = CollegeInfo.objects.get(user=student)
    except CollegeInfo.DoesNotExist:
        college_info = None
    
    try:
        education_info = EducationInfo.objects.filter(user=student)
    except EducationInfo.DoesNotExist:
        education_info = None
    
    try:
        documents = Document.objects.filter(user=student)
    except Document.DoesNotExist:
        documents = None
        

    if request.method == 'POST':
        if "verify" in request.POST:
            student.verification_status = "verified"
            student.save()
        elif "not_verify" in request.POST:
            student.verification_status = "not_verified"
            student.save()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = student
            message.save()
            return redirect('student_detail_admin', pk=pk)
    else:
        form = MessageForm()

    context = {
        'student': student,
        'personal_info': personal_info,
        'college_info': college_info,
        'education_info': education_info,
        'documents': documents,
        'form': form,
    }
    return render(request, 'student_detail_admin.html', context)

def faculty_detail(request, pk):
    faculty = get_object_or_404(CustomUser, pk=pk)

    try:
        personal_info = PersonalInfoFaculty.objects.get(user=faculty)
    except PersonalInfoFaculty.DoesNotExist:
        personal_info = None
        
    if request.method == 'POST':
        if "verify" in request.POST:
            faculty.verification_status = "verified"
            faculty.save()
        elif "not_verify" in request.POST:
            faculty.verification_status = "not_verified"
            faculty.save()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = faculty
            message.save()
            return redirect('faculty_detail', pk=pk)
    else:
        form = MessageForm()

    context = {
        'faculty': faculty,
        'personal_info': personal_info,
        'form': form,
    }
    return render(request, 'faculty_detail.html', context)

class CourseDetailView(DetailView):
    model = Course
    template_name = 'course_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = Student.objects.filter(courses=self.object)
        context['courses'] = Course.objects.all()
        context['personal_info'] = PersonalInfo.objects.filter(profile_picture=self.object)
        return context

class SpecializationDetailView(DetailView):
    model = Specialization
    template_name = 'specialization_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filter students by the current specialization
        context['students'] = Student.objects.filter(specializations=self.object)
        context['courses'] = Course.objects.all()
        return context
    
# main Pages
def recruitmentA(request):
    courses = Course.objects.all()
    return render(request, 'mainA/recruitmentA.html', {
        'courses': courses,
    })

def aboutA(request):
    return render(request, "mainA/aboutA.html")

def coursesA(request):
    return render(request, "mainA/coursesA.html")

def contactA(request):
    return render(request, "mainA/contactA.html")

def iqacA(request):
    return render(request, "mainA/iqacA.html")

def teamA(request):
    return render(request, "mainA/teamA.html")

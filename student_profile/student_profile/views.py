from django.shortcuts import render
from django.contrib.auth import authenticate

from college_admin.models import Course

def index(request):
    if request.user.is_authenticated:
        user = request.user
        if user.user_type == 'faculty':
            return render(request, "facultyindex.html")
        elif user.user_type == 'student':
            return render(request, "studentindex.html")
        elif user.is_superuser:
            return render(request, "adminindex.html")
        else:
            return render(request, "index.html")
    else:
        return render(request, "index.html")
    
def recruitment(request):
    courses = Course.objects.all()
    
    return render(request, 'main/recruitment.html', {
        'courses': courses,
    })
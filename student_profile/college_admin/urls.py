from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.adminindex, name='adminindex'),
    path('dashboard/', views.admin_dash, name='admin_dash'),
    path('home/', views.admin_dash, name='admin_dash'),
    path('verify-students/', views.verify_students_admin, name='verify_students_admin'),
    path('verify-faculty/', views.verify_faculty, name='verify_faculty'),
    path('student/<int:pk>/', views.student_detail_admin, name='student_detail_admin'),
    path('faculty/<int:pk>/', views.faculty_detail, name='faculty_detail'),
    path('create-notice/', views.send_message, name='notice'),
    path('hired/', views.hired_students_view, name='hiredstudent'),

    path('enrollment_chart_data/', views.enrollment_chart_data, name='enrollment_chart_data'),
    path('analysis', views.analysis, name='analysis'),

    path('recruitment-admin', views.recruitmentA, name='recruitmentA'),
    path('about-admin/', views.aboutA, name='aboutA'),
    path('courses-admin/', views.coursesA, name='coursesA'),
    path('contact-admin/', views.contactA, name='contactA'),
    path('iqac-admin/', views.iqacA, name='iqacA'),
    path('team-admin/', views.teamA, name='teamA'),
]
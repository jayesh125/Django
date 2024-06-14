from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.facultyindex, name='facultyindex'),
    path('dashboard/', views.dashboard_home_faculty, name='dashboard_home_faculty'),
    path('form/<str:tab>/', views.form_view_faculty, name='form_view_faculty'),
    path('verify-faculty-id/', views.verify_faculty_id, name='verify_faculty_id'),

    path('send-notification/', views.send_notification, name='send_notification'),

    path('recruitment-faculty/', views.recruitmentF, name='recruitmentF'),
    path('about-faculty/', views.aboutF, name='aboutF'),
    path('courses-faculty/', views.coursesF, name='coursesF'),
    path('contact-faculty/', views.contactF, name='contactF'),
    path('iqac-faculty/', views.iqacF, name='iqacF'),
    path('team-faculty/', views.teamF, name='teamF'),

    
    path('verify-students/', views.verify_students, name='verify_students'),
    path('student/<int:pk>/', views.student_detail, name='student_detail'),
]

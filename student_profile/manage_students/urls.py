from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.studentindex, name='studentindex'),
    path('recruitment/', views.recruitmentS, name='recruitmentS'),
    path('about/', views.aboutS, name='aboutS'),
    path('courses/', views.coursesS, name='coursesS'),
    path('contact/', views.contactS, name='contactS'),
    path('iqac/', views.iqacS, name='iqacS'),
    path('team/', views.teamS, name='teamS'),

    path('dashboard/', views.dashboard_home, name='dashboard_home'),
    path('verify-student-id/', views.verify_student_id, name='verify_student_id'),
    path('view-profile/', views.view_profile, name='view_profile'),

    path('form/<str:tab>/', views.form_view, name='form_view'),
    path('delete_instance/<str:active_tab>/<int:instance_id>/', views.delete_instance, name='delete_instance'),
    path('delete_personal_info/', views.delete_personal_info, name='delete_personal_info'),
    path('delete_education_info/', views.delete_education_info, name='delete_education_info'),
    path('notifications/', views.view_notifications, name='view_notifications'),

]

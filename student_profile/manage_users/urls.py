from django.contrib import admin
from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index', views.index, name='index'),
    path('recruitment', views.recruitment, name='recruitment'),
    path('about', views.about, name='about'),
    path('courses', views.courses, name='courses'),
    path('contact', views.contact, name='contact'),
    path('iqac', views.iqac, name='iqac'),
    path('team', views.team, name='team'),
    
    #login logout signup urls
    path("register", views.signup, name="signup"),
    path("register_as_student", views.signup_student, name="signupstudent"),
    path("register_as_faculty", views.signup_faculty, name="signupfaculty"),

    path("verify-email/<slug:username>", views.verify_email, name="verify-email"),
    path("resend-otp", views.resend_otp, name="resend-otp"),
    path("login", views.signin, name="signin"),
    path('logout', views.handle_logout, name='logout'),

    path('password-reset/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='main/reset_pass_conf.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='main/reset_pass_complete.html'),
         name='password_reset_complete'),

    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('specialization/<int:pk>/', views.SpecializationDetailView.as_view(), name='specialization_detail'),

    path('student/<slug:username>/', views.student_details, name='student_detail'),
    
]

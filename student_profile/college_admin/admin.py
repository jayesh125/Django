from django.contrib import admin
from .models import AdminUser, Message, Course, Specialization, Student, HiredStudent

# Register your models here.

admin.site.register(HiredStudent)

@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'adminID')
    search_fields = ('username', 'email', 'adminID')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'sent_at')
    list_filter = ('sender', 'recipient', 'sent_at')
    search_fields = ('sender__username', 'recipient__username', 'subject')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'duration')
    search_fields = ('name', 'short_name')

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'description')
    list_filter = ('course',)
    search_fields = ('name', 'course__name')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'enrollment_date')
    search_fields = ('user__username', 'user__email')


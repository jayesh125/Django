from django.contrib import admin
from .models import Notification, PersonalInfoFaculty, SkillsFaculty, AchievementsFaculty, LanguagesFaculty, InterestsFaculty

# Register your models here.

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'sender', 'timestamp')
    list_filter = ('sender', 'timestamp')
    search_fields = ('message',)
    
admin.site.register(PersonalInfoFaculty)
admin.site.register(SkillsFaculty)
admin.site.register(AchievementsFaculty)
admin.site.register(LanguagesFaculty)
admin.site.register(InterestsFaculty)
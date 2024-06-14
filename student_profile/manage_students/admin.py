from django.contrib import admin

from .models import PersonalInfo, Document, EducationInfo, Experience, Project, Skills, Achievements, Languages, Interests, CollegeInfo

# Register your models here.

class CollegeInfoAdmin(admin.ModelAdmin):
    list_display = ('roll_no', 'course', 'specialization')
    list_filter = ('course', 'specialization')
    search_fields = ('roll_no', 'course__name', 'specialization__name')

admin.site.register(CollegeInfo, CollegeInfoAdmin)

admin.site.register(PersonalInfo)
admin.site.register(EducationInfo)
admin.site.register(Document)
admin.site.register(Experience)
admin.site.register(Project)
admin.site.register(Skills)
admin.site.register(Achievements)
admin.site.register(Languages)
admin.site.register(Interests)

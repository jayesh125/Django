from django import forms

from college_admin.models import Course, Specialization
from .models import PersonalInfo, EducationInfo, Document, Experience, Project, Skills, Achievements, Interests, Languages, CollegeInfo
from django.core.exceptions import ValidationError
from django.utils import timezone

class PersonalInfoForm(forms.ModelForm):
    aadhar_front = forms.ImageField(label='Aadhar Card Front', required=False)
    aadhar_back = forms.ImageField(label='Aadhar Card Back', required=False)
    profile_picture = forms.ImageField(label='Profile Picture', required=False)

    class Meta:
        model = PersonalInfo
        fields = ['date_of_birth', 'gender', 'phone_number', 'address', 'aadhar_front', 'aadhar_back', 'profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Select date of birth'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address'}),
            'aadhar_front': forms.FileInput(attrs={'class': 'form-control-file'}),
            'aadhar_back': forms.FileInput(attrs={'class': 'form-control-file'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth:
            today = timezone.now().date()
            age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
            if age < 20:
                raise ValidationError("You must be at least 20 years old to apply.")
        return date_of_birth

class CollegeInfoForm(forms.ModelForm):
    class Meta:
        model = CollegeInfo
        fields = ['roll_no', 'course', 'specialization']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['specialization'].queryset = Specialization.objects.none()

        if 'course' in self.data:
            try:
                course_id = int(self.data.get('course'))
                self.fields['specialization'].queryset = Specialization.objects.filter(course_id=course_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Specialization queryset
        elif self.instance.pk:
            self.fields['specialization'].queryset = self.instance.course.specializations.order_by('name')
          
class EducationInfoForm(forms.ModelForm):
    tenth_school_certificate = forms.ImageField(label='10th Certificate', required=False)
    twelfth_school_certificate = forms.ImageField(label='12th Certificate', required=False)
    degree_certificate = forms.ImageField(label='Degree Certificate', required=False)

    class Meta:
        model = EducationInfo
        fields = ['tenth_school', 'tenth_year', 'tenth_percentage', 'tenth_school_certificate', 
                  'twelfth_school', 'twelfth_year', 'twelfth_percentage', 'twelfth_school_certificate', 
                  'degree_college', 'degree_course', 'degree_year', 'degree_certificate']
        labels = {
            'tenth_school': '10th School',
            'tenth_year': '10th Year',
            'tenth_percentage': '10th Percentage',
            'twelfth_school': '12th/ Diploma School',
            'twelfth_year': '12th/ Diploma Year',
            'twelfth_percentage': '12th/ Diploma Percentage',
            'degree_college': 'College/University',
            'degree_course': 'Degree/Course',
            'degree_year': 'Degree Year',
            'degree_certificate': 'Degree Certificate',
        }
        widgets = {
            'tenth_school': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter 10th school'}),
            'tenth_year': forms.Select(attrs={'class': 'form-control'}),
            'tenth_percentage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter 10th percentage'}),
            'tenth_school_certificate': forms.FileInput(attrs={'class': 'form-control-file'}),
            'twelfth_school': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter 12th school'}),
            'twelfth_year': forms.Select(attrs={'class': 'form-control'}),
            'twelfth_percentage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter 12th percentage'}),
            'twelfth_school_certificate': forms.FileInput(attrs={'class': 'form-control-file'}),
            'degree_college': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter college/university'}),
            'degree_course': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter degree/course'}),
            'degree_year': forms.Select(attrs={'class': 'form-control'}),
            'degree_certificate': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document_type', 'document_file']
        widgets = {
            'document_type': forms.Select(attrs={'class': 'form-control'}),
            'document_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ExperienceForm(forms.ModelForm):
    certificate = forms.ImageField(label='Certificate', required=False)

    class Meta:
        model = Experience
        fields = ['job_title', 'company_name', 'start_date', 'end_date', 'description', 'certificate']
        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter job title'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter company name'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Select start date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Select end date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description', 'rows': 3}),
            'certificate': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'start_date', 'end_date', 'description', 'project_document', 'project_links']
        widgets = {
            'project_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project name'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Select start date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Select end date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description', 'rows': 3}),
            'project_document': forms.FileInput(attrs={'class': 'form-control-file'}),
            'project_links': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter project links (separated by commas)'}),
        }

class SkillsForm(forms.ModelForm):
    skill_certificate = forms.ImageField(label='Skill Certificate', required=False)

    class Meta:
        model = Skills
        fields = ['skill_name', 'proficiency_level', 'skill_certificate']
        widgets = {
            'skill_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter skill name'}),
            'proficiency_level': forms.Select(attrs={'class': 'form-control'}),
        }

class AchievementsForm(forms.ModelForm):
    achievement_certificate = forms.ImageField(label='Achievement Certificate', required=False)

    class Meta:
        model = Achievements
        fields = ['achievement_title', 'description', 'achievement_certificate']
        widgets = {
            'achievement_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter achievement title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description', 'rows': 3}),
        }

class InterestsForm(forms.ModelForm):
    interest_certificate = forms.ImageField(label='Interest Certificate', required=False)

    class Meta:
        model = Interests
        fields = ['interest', 'interest_certificate']
        widgets = {
            'interest': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter interest'}),
        }

class LanguagesForm(forms.ModelForm):
    language_certificate = forms.ImageField(label='Language Certificate', required=False)

    class Meta:
        model = Languages
        fields = ['language', 'proficiency', 'language_certificate']
        widgets = {
            'language': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter language'}),
            'proficiency': forms.Select(attrs={'class': 'form-control'}),
        }


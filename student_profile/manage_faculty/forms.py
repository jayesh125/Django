from .models import CustomUser, Notification
from .models import PersonalInfoFaculty, SkillsFaculty, InterestsFaculty, AchievementsFaculty, LanguagesFaculty
from django import forms


class NotificationForm(forms.ModelForm):
    recipients = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.filter(user_type='student'))

    class Meta:
        model = Notification
        fields = ['message', 'recipients']

class PersonalInfoForm(forms.ModelForm):
    aadhar_front = forms.ImageField(label='Aadhar Card Front', required=False)
    aadhar_back = forms.ImageField(label='Aadhar Card Back', required=False)
    profile_picture = forms.ImageField(label='Profile Picture', required=False)

    class Meta:
        model = PersonalInfoFaculty
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

class SkillsForm(forms.ModelForm):
    skill_certificate = forms.ImageField(label='Skill Certificate', required=False)

    class Meta:
        model = SkillsFaculty
        fields = ['skill_name', 'proficiency_level', 'skill_certificate']
        widgets = {
            'skill_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter skill name'}),
            'proficiency_level': forms.Select(attrs={'class': 'form-control'}),
        }

class AchievementsForm(forms.ModelForm):
    achievement_certificate = forms.ImageField(label='Achievement Certificate', required=False)

    class Meta:
        model = AchievementsFaculty
        fields = ['achievement_title', 'description', 'achievement_certificate']
        widgets = {
            'achievement_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter achievement title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description', 'rows': 3}),
        }

class InterestsForm(forms.ModelForm):
    interest_certificate = forms.ImageField(label='Interest Certificate', required=False)

    class Meta:
        model = InterestsFaculty
        fields = ['interest', 'interest_certificate']
        widgets = {
            'interest': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter interest'}),
        }

class LanguagesForm(forms.ModelForm):
    language_certificate = forms.ImageField(label='Language Certificate', required=False)

    class Meta:
        model = LanguagesFaculty
        fields = ['language', 'proficiency_level', 'language_certificate']
        widgets = {
            'language': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter language'}),
            'proficiency': forms.Select(attrs={'class': 'form-control'}),
        }

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from manage_users.models import VerificationID 

class RegisterForm(UserCreationForm):
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={"placeholder": "Enter email-address", "class": "form-control"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter username", "class": "form-control"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter first name", "class": "form-control"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter last name", "class": "form-control"}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Enter password", "class": "form-control"}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={"placeholder": "Confirm password", "class": "form-control"}))
    
    class Meta:
        model = get_user_model()
        fields = ["email", "username", "first_name", "last_name", "password1", "password2"]

class RegisterFormStudent(UserCreationForm):
    student_id = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Enter student ID", "class": "form-control"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"placeholder": "Enter email-address", "class": "form-control"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter username", "class": "form-control"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter first name", "class": "form-control"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter last name", "class": "form-control"}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Enter password", "class": "form-control"}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={"placeholder": "Confirm password", "class": "form-control"}))
    
    class Meta:
        model = get_user_model()
        fields = ["email", "username", "first_name", "last_name", "password1", "password2", "student_id"]

class RegisterFormFaculty(UserCreationForm):
    faculty_id = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter Faculty ID", "class": "form-control"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"placeholder": "Enter email-address", "class": "form-control"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter username", "class": "form-control"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter first name", "class": "form-control"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter last name", "class": "form-control"}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Enter password", "class": "form-control"}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={"placeholder": "Confirm password", "class": "form-control"}))

    class Meta:
        model = get_user_model()
        fields = ["email", "username", "first_name", "last_name", "password1", "password2", "faculty_id"]

class FacultyIDVerificationForm(forms.Form):
    faculty_id = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter Faculty ID", "class": "form-control"}))

    def clean_faculty_id(self):
        faculty_id = self.cleaned_data.get('faculty_id')
        if not VerificationID.objects.filter(id_type='faculty', id_value=faculty_id).exists():
            raise forms.ValidationError("Invalid faculty ID")
        return faculty_id
    
class EmailForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    
    
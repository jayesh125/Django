from django import forms
from .models import Course, Message, CustomUser, Specialization

class MessageForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), required=False)
    specialization = forms.ModelChoiceField(queryset=Specialization.objects.all(), required=False)
    send_to_all = forms.BooleanField(required=False, label="Send to all students")

    class Meta:
        model = Message
        fields = ['subject', 'body', 'course', 'specialization', 'send_to_all']

    def get_filtered_recipients(self):
        send_to_all = self.cleaned_data.get('send_to_all')
        
        if send_to_all:
            return CustomUser.objects.filter(user_type='student')
        
        course = self.cleaned_data.get('course')
        specialization = self.cleaned_data.get('specialization')
        
        recipients = CustomUser.objects.filter(user_type='student')
        
        if course:
            recipients = recipients.filter(course=course)
        if specialization:
            recipients = recipients.filter(specialization=specialization)
        
        return recipients
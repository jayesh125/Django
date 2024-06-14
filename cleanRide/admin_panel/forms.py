from django import forms
from admin_panel.models import BlogPost
from shop.models import OrderPlaced

class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderPlaced
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        # Ensure other fields are not marked as read-only or disabled
        for field in self.fields:
            self.fields[field].widget.attrs.pop('readonly', None)
            self.fields[field].widget.attrs.pop('disabled', None)
            
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'author', 'date_posted', 'image', 'content']
        widgets = {
            'date_posted': forms.DateInput(attrs={'type': 'date'}),
        }
        
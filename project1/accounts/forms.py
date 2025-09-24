from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields have form-control class for Bootstrap styling
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields have form-control class for Bootstrap styling
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
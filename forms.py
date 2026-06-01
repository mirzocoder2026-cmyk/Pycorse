from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, label='Ном')
    last_name  = forms.CharField(max_length=50, label='Насаб')
    email      = forms.EmailField(label='Почта')
    class Meta:
        model  = CustomUser
        fields = ('username','first_name','last_name','email','password1','password2')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs['class'] = 'form-input'

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-input','placeholder':'Логин'})
        self.fields['password'].widget.attrs.update({'class':'form-input','placeholder':'Парол'})

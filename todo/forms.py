from django import forms
from django.contrib.auth.models import User
from .models import Todo

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password'
        ]

class TodoForm(forms.ModelForm):
    class Meta:
        model=Todo
        fields = [
            'title',
            'description'
        ]

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Enter Todo Title'
                }
            ),

            'description':forms.Textarea(
                attrs={
                    'class':'form-control',
                    'placeholder':'Enter Description',
                    'rows':3
                }
            )
        }
        
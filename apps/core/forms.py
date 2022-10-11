from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms 

class CreationUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email')
        widgets = {
            'username': forms.TextInput(attrs={
                        'class':'input',
                        'placeholder':'Entrez votre username',
                }),
            'email': forms.EmailInput(attrs={
                        'class':'input',
                        'placeholder':'Entrez votre email',
                }),

        }
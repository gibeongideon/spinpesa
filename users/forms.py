
from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
#from .models import User
from django.contrib.auth import get_user_model

User = get_user_model()
class LoginForm2(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",                
                "class"       : "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",
                "class"       : "form-control"
            }
        ))

class SignUpForm2(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",                
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email",                
                "class": "form-control"
            }
        ))
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Phone_number",                
                "class": "form-control"
            }
        ))
    daru_code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "daru_code",                
                "class": "form-control"
            }
        ))
    # last_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "placeholder" : "Refer Code",                
    #             "class": "form-control"
    #         }
    #     ))

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password check",                
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email','last_name', 'password1', 'password2')
        
        
        
        
        
        
        
        


class SignUpForm(UserCreationForm):
    """Prepares help texts, class and placeholder attributes.

    Define methods to increase and decrese token_count amount,
    betting and check if bet is possible.
    """

    username = forms.CharField(max_length=50, required=True,
        label='', help_text='Required. Inform unique username',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username...'
        }))

    # first_name = forms.CharField(max_length=30, required=False,
    #     label='', help_text='Optional',
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control',
    #         'placeholder': 'First name...'
    #     }))

    # last_name = forms.CharField(max_length=30, required=False,
    #     label='', help_text='Optional',
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control',
    #         'placeholder': 'Last name...'
    #     }))

    phone_number = forms.CharField(max_length=150, required=False,
        label='',
        help_text='Start with 254 i.e 254700000000.Confirm before you register',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number...'
        }))

    email = forms.EmailField(max_length=254, required=True,
        label='', help_text='Required. Inform a valid email unique address.',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email...'
        }))

    password1 = forms.CharField(required=True,
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password...'
        }))

    password2 = forms.CharField(required=True,
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password...'
        }))

    class Meta:
        model = User
        fields = ('username', 'phone_number',
            'email', 'password1', 'password2')

        

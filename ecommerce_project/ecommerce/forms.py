from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer
from django.contrib.auth.forms import AuthenticationForm

class CustomUserCreationForm(forms.ModelForm):
    user_name = forms.CharField(max_length=150)
    first_name = forms.CharField(
        max_length=30, required=True,
        help_text="Required. Enter your first name.",
        widget=forms.TextInput(attrs={'class': 'form-control'}) 
    )
    last_name = forms.CharField(
        max_length=30, required=True,
        help_text="Required. Enter your last name.",
        widget=forms.TextInput(attrs={'class': 'form-control'}) 
    )
    email = forms.EmailField(
        max_length=254, required=True,
        help_text="Required. Enter a valid email address.",
        widget=forms.EmailInput(attrs={'class': 'form-control'})  
    )
    class Meta:
        model = Customer  
        fields = ('user_name', 'first_name', 'last_name', 'email', 'password')

class CustomUserLogin(forms.ModelForm):
    email = forms.EmailField(
        max_length=254, required=True,
        help_text="Required. Enter a valid email address.",
        widget=forms.EmailInput(attrs={'class': 'form-control'})  
    )
    class Meta:
        model = Customer  
        fields = ('email', 'password')

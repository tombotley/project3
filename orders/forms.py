from django import forms
from django.forms import widgets


class Registration(forms.Form):
    # add validation such as max lengths
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="First name", empty_value = "enter your first name")
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Last name", empty_value = "enter your last name")
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Username", empty_value = "choose your username")
    email = forms.EmailField(widget=widgets.EmailInput(attrs={'class': 'form-control'}), label="Email address", empty_value="enter your email")
    password = forms.CharField(widget=widgets.PasswordInput(attrs={'class': 'form-control'}), label="Password", empty_value = "choose a password")
    confirm_pw = forms.CharField(widget=widgets.PasswordInput(attrs={'class': 'form-control'}), label="Confirm password", empty_value="confirm your password")


class Login(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Username", empty_value="enter username")
    password = forms.CharField(widget=widgets.PasswordInput(attrs={'class': 'form-control'}), label="Password", empty_value="enter password")
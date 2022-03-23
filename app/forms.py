from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Account
from app.models import Expenses

class LoginForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        """
        will only continue if form is valid

        get email and password from form and authenticate the user
        
        if return True, do nothing the login process will happen at the view.py file

        if not raise validation error and tell user what is wrong
        """
        if self.is_valid:
            clean_email = self.cleaned_data.get('email')
            clean_password = self.cleaned_data.get('password')
            user = authenticate(email = clean_email, password = clean_password)
            if user:
                pass
            else:
                raise forms.ValidationError("Email or Password Might Be Wrong")

class RegisterForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('email','username','password1','password2','currency')

    def clean_email(self):
        if self.is_valid():
            clean_email = self.cleaned_data['email']
            try:
                exist_email = Account.objects.get(email = clean_email)
                if exist_email:
                    raise forms.ValidationError('{} has been registered by others'.format(clean_email))
            except:
                return clean_email

class UpdateDetailForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('email','username')

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data.get('email')
            try:
                email_exist = Account.objects.get(email = email).exclude(pk = self.instance.id)
                if email_exist:
                    raise forms.ValidationError('Email of "{}" has been registered'.format(email))
            except:
                return email


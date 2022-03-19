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
            clean_email = self.cleaned_data['email']
            clean_password = self.cleaned_data['password']
            user = authenticate(email = clean_email, password = clean_password)
            if user:
                pass
            else:
                raise forms.ValidationError("Email or Password Might Be Wrong")

class SignUpForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('email', 'username', 'password1','password2')

    def clean(self):
        if self.is_valid:
            """
                will only continue if form is valid
                get email,username password1 and password2 from form

                comparision of password 1 and 2 will be take care in UserCreationFrom

                need to check if the email exists in the database(others had register it before)

            """
            clean_email = self.cleaned_data["email"]
            try:
                email_exists = Account.objects.get(email=clean_email)
                if email_exists:
                    raise forms.ValidationError("{} had been used registered".format(clean_email))
            except:
                return clean_email



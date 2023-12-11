from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile

class UserRegistrationForm (forms.Form):

    username = forms.CharField( max_length=20 , required=True , widget=forms.TextInput(attrs={'class':'form-control' , 'placeholder' : 'your username'}))
    password1 = forms.CharField(label='password' , min_length=5, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'your password'}))
    password2 = forms.CharField(label='confirm password', min_length=5 , widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'your password'}))
    email = forms.EmailField( widget=forms.EmailInput(attrs={'class':'form-control' , 'placeholder' : 'your email'}))
    first_name = forms.CharField( max_length=20 , widget=forms.TextInput(attrs={'class':'form-control' , 'placeholder' : 'Jason'}))
    last_name = forms.CharField( max_length=20 , widget=forms.TextInput(attrs={'class':'form-control' , 'placeholder' : 'Stathom'}))
    comment = forms.CharField( widget=forms.Textarea , required=False)

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email already exist')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('This username already exist')
        return username

    def clean(self):
        new = super().clean()
        p1 = new.get('password1')
        p2 = new.get('password2')

        if p1 and p2 and p1 != p2 :
            raise ValidationError('Passwords not match')

class UserLoginForm (forms.Form):

    username = forms.CharField(max_length=20, required=True,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}))
    password = forms.CharField( min_length=5, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}))


class EditUserProfileForm (forms.ModelForm):
    email = forms.EmailField() 
    class  Meta:
        model = Profile
        fields = [ 'job' , 'city' , 'country' , 'image' , 'age'  , 'bio']
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review, Request, Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ReviewForm(forms.ModelForm):
   class Meta:
       model = Review
       fields = ('title', 'content', 'stars', 'movie')
       user = User

class ProfileForm(forms.ModelForm):
   class Meta:
       model = Profile
       fields = ('bio', 'image', 'websiteurl', 'twitterurl', 'instagramurl', 'facebookurl', 'private')
       user = User

class ContactForm(forms.ModelForm):
   class Meta:
       model = Request
       fields = ('subject', 'content')
       user = User


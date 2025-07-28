from django import forms
from .models import Movie, Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['movie', 'rating', 'text']  # Use 'text' not 'comment'
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5}),
        }
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'release_date', 'genre']


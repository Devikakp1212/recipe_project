from django import forms
from .models import Recipe, Comment,Rating
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

        widgets = {

            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Username'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Email'
            }),
        }
    

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['category', 'title', 'image', 'video',
                  'ingredients', 'instructions']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
class RatingForm(forms.ModelForm):

    CHOICES = [
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    ]

    rating = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:
        model = Rating
        fields = ['rating']

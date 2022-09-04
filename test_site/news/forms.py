from django import forms

from .models import *

class ReviewNewsForm(forms.ModelForm):
    class Meta:
        model = ReviewsNews
        fields = ('name', 'email', 'text')


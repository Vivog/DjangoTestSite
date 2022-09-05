from django import forms

from .models import *


class ReviewProjectForm(forms.ModelForm):
    class Meta:
        model = ReviewsProjects
        fields = ('name', 'email', 'text')
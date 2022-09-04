from django import forms

from .models import *


class ReviewPubForm(forms.ModelForm):
    class Meta:
        model = ReviewsPubs
        fields = ('name', 'email', 'text')
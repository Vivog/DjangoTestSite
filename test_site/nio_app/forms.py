import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *

class ReviewPubForm(forms.ModelForm):
    class Meta:
        model = ReviewsPubs
        fields = ('name', 'email', 'text')






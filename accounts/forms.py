from django import forms
from django.core.files.base import File
from django.db.models import query
from django.db.models.expressions import Col
from django.db.models.fields import BLANK_CHOICE_DASH
from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, Submit, HTML, Field
from django.core.exceptions import ValidationError
# from .validators import validate_file_extension, valid_extensions
import re
import datetime
import pytz

class SignUpForm(forms.ModelForm):

    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Confirm Password'
        )

    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'date_joined':forms.DateTimeInput()
        }


    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['date_joined'].widget = widgets.HiddenInput()
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('username'),
            ),
            Row(
                Column('password'),
            ),
            Row(
                Column('password2'),
            ),
            Row(
                Column('date_joined'),
            ),
            Submit('submit', 'Signup'),
        )
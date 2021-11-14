from django import forms
from django.core.files.base import File
from django.db.models import query
from django.db.models.expressions import Col
from django.db.models.fields import BLANK_CHOICE_DASH
from django.forms import widgets
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, Submit, HTML, Field
from django.core.exceptions import ValidationError
from .validators import validate_file_extension, valid_extensions
import re
import datetime
import pytz


class UploadDataFrame(forms.ModelForm):

    dataframe = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=True)
    
    
    class Meta:
        model = DataFrame
        fields = '__all__'
        widgets = {
            'creator': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        creator = kwargs.pop('creator')
        super(UploadDataFrame, self).__init__(*args, **kwargs)
        self.fields['dataframe'].help_text = valid_extensions()
        self.helper = FormHelper(self)
        self.fields['creator'].initial = creator
        self.helper.layout = Layout(
            'creator',
            Row(
                Column('name'),
            ),
            Row(
                Column('dataframe')
            ),
            Submit('submit', 'Submit'),
        )
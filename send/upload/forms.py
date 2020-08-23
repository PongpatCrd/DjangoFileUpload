from django import forms

import os
import re

from .models import *

class UploadForm(forms.ModelForm):
  file = forms.FileField()
  max_downloads = forms.ChoiceField(
    choices=[
      (1, '1 download'),
      (2, '2 downloads'),
      (3, '3 downloads'),
      (4, '4 downloads'),
      (5, '5 downloads'),
      (20, '20 downloads'),
      (50, '50 downloads'),
      (100, '100 downloads'),
    ]
  )
  expire_duration = forms.ChoiceField(
    choices=[
      (5 * 60, '5 minutes'),
      (60 * 60, '1 hour'),
      (24 * 60 * 60, '1 day'),
      (7 * 24 * 60 * 60, '7 days'),
    ]
  )
  
  class Meta:
    model = Upload
    fields = ['password', 'max_downloads', 'file']
    widgets = {
      'password': forms.PasswordInput(attrs={
        'minlength': 8,
      }),
    }

  def clean_password(self):
    password = self.cleaned_data.get('password')

    if password:
      if len(password) > 16:
        raise forms.ValidationError('Password must be in length 8-16')
      if not re.match('^[a-zA-Z0-9_]*$', password):
        raise forms.ValidationError('Password field has invalid pattern, Please use only in these pattern [A-Z, a-z, 0-9, _]')
    
    return password

  def clean_file(self):
    size_limit_in_byte = 104857600
    content = self.cleaned_data.get('file')
    
    if content.size > size_limit_in_byte:
      raise forms.ValidationError(f'File is too big, We only accept file that lower or equal {size_limit_in_byte/(1024*2)} MB')

    return content
    

class DownloadForm(forms.ModelForm):
  class Meta:
    model = Upload
    fields = ['password']
    widgets = {
      'password': forms.PasswordInput(attrs={
        'minlength': 8,
      }),
    }

  def clean_password(self):
    password = self.cleaned_data.get('password')

    if password:
      if len(password) > 16:
        raise forms.ValidationError('Password must be in length 8-16')
      if not re.match('^[a-zA-Z0-9_]*$', password):
        raise forms.ValidationError('Password field has invalid pattern, Please use only in these pattern [A-Z, a-z, 0-9, _]')

    return password
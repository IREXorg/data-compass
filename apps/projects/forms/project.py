from django import forms
from django.forms import ModelForm

from ..models import Project

class ProjectCreateForm(ModelForm):
    """
    Project create form
    """
    class Meta:
        model = Project
        fields = ['name', 'description', 'email', 'tags', ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }

class ProjectUpdateForm(ModelForm):
    """
    Project create form
    """
    class Meta:
        model = Project
        fields = ['name', 'description', ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }


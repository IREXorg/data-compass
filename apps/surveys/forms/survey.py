from django.forms import ModelForm

from ..models import Survey


class SurveyCreateForm(ModelForm):
    """
    Survey create form
    """
    class Meta:
        model = Survey
        fields = ['name', 'description', 'display_name']


class SurveyUpdateForm(ModelForm):
    """
    Survey update form
    """
    class Meta:
        model = Survey
        fields = ['name', 'description', 'display_name']

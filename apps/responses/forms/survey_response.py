from django import forms

from ..models import SurveyResponse


class SurveyResponseCompleteForm(forms.ModelForm):

    class Meta:
        model = SurveyResponse
        fields = ['completed_at']
        widgets = {
            'completed_at': forms.HiddenInput()
        }

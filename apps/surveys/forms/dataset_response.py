from django import forms
from django.utils.translation import ugettext_lazy as _

from ..models import DatasetResponse


class DatasetSelectForm(forms.Form):
    datasets = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        label=_('In my everday work, I usually encounter information about:'),
    )

    def __init__(self, survey=None, survey_response=None, *args, **kwargs):
        self.survey_response = survey_response

        # get project inorder to limit hierarchy choices
        if not survey:
            raise ValueError(_(f'Survey must be specified to initialize {self.__class__.__name__}'))

        super().__init__(*args, **kwargs)
        if survey_response:
            self.initial['datasets'] = survey_response.get_datasets()

        self.fields['datasets'].queryset = survey.datasets.all()


class DatasetResponseForm(forms.ModelForm):
    dataset_frequency = forms.ModelChoiceField(
        queryset=None,
        widget=forms.RadioSelect,
        required=True,
        empty_label=None
    )

    class Meta:
        model = DatasetResponse
        fields = '__all__'

    def __init__(self, survey=None, survey_response=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if survey:
            self.fields['dataset_frequency'].queryset = survey.dataset_frequencies.all()
        elif self.instance:
            self.fields['dataset_frequency'].queryset = self.instance.response.survey.dataset_frequencies.all()


class DatasetResponseFrequencyForm(DatasetResponseForm):

    class Meta:
        model = DatasetResponse
        fields = ['dataset_frequency']

    def __init__(self, survey=None, survey_response=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['dataset_frequency'].label = _(
                'How often do you produce, access or share information '
                'about %(dataset_name)s?'
            ) % {'dataset_name': self.instance.dataset.name}

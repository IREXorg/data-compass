from django import forms
from django.utils.translation import ugettext_lazy as _

from ..models import DatasetResponse, DatasetTopicResponse, DatasetTopicStorageAccess, Role


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
                'about %(dataset)s?'
            ) % {'dataset': self.instance.dataset.name}


class DatasetTopicResponseForm(forms.ModelForm):

    percieved_owner = forms.ModelChoiceField(
        queryset=None,
        widget=forms.RadioSelect,
        required=True,
        empty_label=None
    )

    class Meta:
        model = DatasetTopicResponse
        fields = ['percieved_owner']

    def __init__(self, project=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['percieved_owner'].label = _(
                'Who at %(hierarchy)s do you believe knows most '
                'about %(topic)s regarding %(dataset)s?'
            ) % {
                'dataset': self.instance.dataset_response.dataset.name,
                'hierarchy': self.instance.dataset_response.respondent.hierarchy,
                'topic': self.instance.topic.name
            }

        if not project and self.instance:
            project = self.instance.dataset_response.response.survey.project

        self.fields['percieved_owner'].queryset = Role.objects.filter(hierarchy__project=project)


class DatasetTopicStorageAccessForm(forms.ModelForm):
    selected = forms.BooleanField(required=False)

    class Meta:
        model = DatasetTopicStorageAccess
        fields = ['selected', 'storage', 'access']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.storage_name = None

        if self.initial:
            storage = self.initial.get('storage')
            if storage:
                self.storage_name = storage.name

        self.fields['access'].required = False

    def clean(self):
        super().clean()

        if self.cleaned_data['selected']:
            if not self.cleaned_data['access']:
                raise forms.ValidationError(_('Please please specify how this is accessible'))


class BaseDatasetTopicStorageAccessFormSet(forms.BaseModelFormSet):

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = None
        self.can_delete = False
        self.instance = instance

        if self.instance:
            self.queryset = self.instance.storages.all()

            storages = self.instance.dataset_response.response.survey.dataset_storages.all()

            # set number of forms equal to storage options
            self.extra = self.max_num = len(storages)

            self.initial = [{'storage': storage} for storage in storages]

            initial_selected = self.instance.storages.select_related('access', 'storage')
            initial_storages = [item.storage for item in initial_selected]

            for item in self.initial:
                try:
                    i = initial_storages.index(item['storage'])
                    item['selected'] = True
                    item['access'] = initial_selected[i].access
                except ValueError:
                    item['access'] = None
                    pass

    def save(self):
        if not self.instance:
            raise ValueError(_('Instance not specified'))

        saved_forms = []

        # clear existing records
        self.instance.storages.all().delete()

        # save each of the selected records
        for form in self.forms:
            if form.cleaned_data.get('selected'):
                form.instance.response = self.instance
                saved_forms.append(form.save())

        return saved_forms


DatasetTopicStorageAccessFormSet = forms.modelformset_factory(
    DatasetTopicStorageAccess,
    form=DatasetTopicStorageAccessForm,
    formset=BaseDatasetTopicStorageAccessFormSet
)

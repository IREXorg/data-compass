from django import forms
from django.utils.translation import ugettext_lazy as _

from apps.surveys.models import DatasetFrequency, Role, Topic

from ..models import (DatasetResponse, DatasetTopicReceived, DatasetTopicResponse, DatasetTopicShared,
                      DatasetTopicStorageAccess)


class DatasetSelectForm(forms.Form):
    datasets = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        label=_('In my everday work, I usually encounter information about:'),
    )

    def __init__(self, survey=None, survey_response=None, *args, **kwargs):
        self.survey_response = survey_response

        # get survey in order to limit hierarchy choices
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
        else:
            self.fields['dataset_frequency'].queryset = DatasetFrequency.objects.none()


class DatasetResponseFrequencyForm(DatasetResponseForm):

    class Meta:
        model = DatasetResponse
        fields = ['dataset_frequency']

    def __init__(self, survey=None, survey_response=None, *args, **kwargs):
        super().__init__(survey=survey, *args, **kwargs)
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

    def __init__(self, survey=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['percieved_owner'].label = _(
                'Who at %(hierarchy)s do you believe knows <u>the most</u> '
                'about %(topic)s regarding %(dataset)s?'
            ) % {
                'dataset': self.instance.dataset_response.dataset.name,
                'hierarchy': self.instance.dataset_response.respondent.hierarchy,
                'topic': self.instance.topic.name
            }

        if not survey and self.instance:
            survey = self.instance.dataset_response.response.survey

        self.fields['percieved_owner'].queryset = Role.objects.filter(survey=survey)


class DatasetTopicStorageAccessForm(forms.ModelForm):
    selected = forms.BooleanField(required=False)

    class Meta:
        model = DatasetTopicStorageAccess
        fields = ['selected', 'storage', 'access']

    def __init__(self, survey=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.storage_name = None

        if self.initial:
            storage = self.initial.get('storage')
            if storage:
                self.storage_name = storage.name

        self.fields['access'].required = False
        self.fields['storage'].queryset = survey.dataset_storages.all()
        self.fields['access'].queryset = survey.dataset_access.all()

    def clean(self):
        super().clean()

        if self.cleaned_data['selected']:
            if not self.cleaned_data['access']:
                raise forms.ValidationError(_('Please specify how this is accessible'))


class BaseDatasetTopicStorageAccessFormSet(forms.BaseModelFormSet):

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = None
        self.can_delete = False
        self.instance = instance

        if self.instance:
            self.queryset = self.instance.storages.all()
            self.form_kwargs['survey'] = self.instance.dataset_response.response.survey

            storages = self.instance.dataset_response.response.survey.dataset_storages.all()

            # set number of forms equal to storage options
            self.extra = self.max_num = len(storages)

            self.initial = [{'storage': storage} for storage in storages]

            initial_selected = self.instance.storages.select_related('access', 'storage')
            initial_storages = [item.storage for item in initial_selected]

            if not self.is_bound:
                for item in self.initial:
                    try:
                        i = initial_storages.index(item['storage'])
                        item['selected'] = True
                        item['access'] = initial_selected[i].access
                    except ValueError:
                        item['access'] = None

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


class DatasetTopicSharedForm(forms.ModelForm):
    selected = forms.BooleanField(required=False)

    class Meta:
        model = DatasetTopicShared
        fields = ['selected', 'entity', 'topic']

    def __init__(self, survey=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.entity_name = None

        if self.initial:
            entity = self.initial.get('entity')
            if entity:
                self.entity_name = entity.name

        self.fields['topic'].required = False

        if survey:
            self.fields['topic'].queryset = survey.topics.all()
        else:
            self.fields['topic'].queryset = Topic.objects.none()

    def clean(self):
        super().clean()
        if self.cleaned_data['selected']:
            if not self.cleaned_data['topic']:
                raise forms.ValidationError(_('Please specify topic'))


class BaseDatasetTopicSharedFormSet(forms.BaseModelFormSet):

    def __init__(self, instance=None, survey=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = None
        self.can_delete = False
        self.instance = instance

        if self.instance:
            self.queryset = self._get_queryset()

            survey = survey or self.instance.dataset_response.response.survey
            entities = survey.entities.all()

            self.form_kwargs['survey'] = survey

            # set number of forms equal to entity options
            self.extra = self.max_num = len(entities)

            self.initial = [{'entity': entity} for entity in entities]

            initial_selected = self.get_initial_selected()
            initial_entities = [item.entity for item in initial_selected]

            # if form is unbound setup the initial data
            if not self.is_bound:
                for item in self.initial:
                    try:
                        i = initial_entities.index(item['entity'])
                        item['selected'] = True
                        item['topic'] = initial_selected[i].topic
                    except ValueError:
                        item['topic'] = None

    def save(self):
        if not self.instance:
            raise ValueError(_('Instance not specified'))

        saved_forms = []

        # clear existing records
        self.clear_entities()

        # save each of the selected records
        for form in self.forms:

            if form.cleaned_data.get('selected'):
                form.instance.dataset_response = self.instance
                saved_forms.append(form.save())

        return saved_forms

    def _get_queryset(self):
        return self.instance.datasettopicshared_set.all()

    def get_initial_selected(self):
        return self.instance.datasettopicshared_set.select_related('entity', 'topic')

    def clear_entities(self):
        self.instance.shared_to.clear()


DatasetTopicSharedFormSet = forms.modelformset_factory(
    DatasetTopicShared,
    form=DatasetTopicSharedForm,
    formset=BaseDatasetTopicSharedFormSet
)


class DatasetTopicReceivedForm(DatasetTopicSharedForm):

    class Meta:
        model = DatasetTopicReceived
        fields = ['selected', 'entity', 'topic']


class BaseDatasetTopicReceivedFormSet(BaseDatasetTopicSharedFormSet):

    def _get_queryset(self):
        return self.instance.datasettopicreceived_set.all()

    def get_initial_selected(self):
        return self.instance.datasettopicreceived_set.select_related('entity', 'topic')

    def clear_entities(self):
        self.instance.received_from.clear()


DatasetTopicReceivedFormSet = forms.modelformset_factory(
    DatasetTopicReceived,
    form=DatasetTopicReceivedForm,
    formset=BaseDatasetTopicReceivedFormSet
)

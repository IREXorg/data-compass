from django import forms
from django.forms import ModelForm
from django.templatetags.static import static
from django.utils.translation import ugettext_lazy as _

import xlrd

from apps.respondents.models import Respondent
from apps.users.models import User

from ..models import HierarchyLevel, Survey


class RespondentCreateForm(ModelForm):
    """
    Basic Respondent create form
    """

    class Meta:
        model = Respondent
        fields = ['survey', 'email', 'hierarchy_level']
        widgets = {
            'survey': forms.HiddenInput(),
        }
        labels = {
            'email': _('Email Address'),
            'hierarchy_level': _('System Hierarchy Level'),
        }

    def __init__(self, survey=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        if survey:
            self.initial['survey'] = survey
            self.fields['hierarchy_level'].queryset = survey.project.hierarchy_levels.all()

    def save(self, commit=True):
        respondent = super().save(commit=commit)

        # link respondent with user if exists
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            respondent.user = user
            respondent.save()

        return respondent


class RespondentUpdateForm(ModelForm):
    """
    Basic Respondent update form
    """
    class Meta:
        model = Respondent
        fields = ['email', 'hierarchy_level']
        widgets = {}
        labels = {
            'email': _('Email Address'),
            'hierarchy_level': _('System Hierarchy Level'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['hierarchy_level'].required = True
        self.fields['hierarchy_level'].queryset = self.instance.survey.project.hierarchy_levels.all()

    def save(self, commit=True):
        respondent = super().save(commit=commit)

        # link respondent with user if exists
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            respondent.user = user
            respondent.save()

        return respondent


class RespondentsUploadForm(ModelForm):
    """
    Basic Respondent(s) upload form
    """
    respondents_file_help_text = _(
        'Please upload respondents. '
        '<a href="%(template_url)s" download>Click here for respondents file template</a>.'
    ) % {'template_url': static('files/templates/respondents.xlsx')}

    respondents_file = forms.FileField(
        label=_('Respondents'),
        required=True,
        help_text=respondents_file_help_text
    )

    respondents_creator = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Survey
        fields = ['respondents_creator', 'respondents_file']
        widgets = {}
        labels = {}

    def __init__(self, creator=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['respondents_file'].required = True
        if creator:
            self.initial['respondents_creator'] = creator.pk

    def clean_respondents_file(self):
        """
        Returns respondents from uploaded excel file
        """
        uploaded_respondents_file = self.cleaned_data['respondents_file']

        try:
            book = xlrd.open_workbook(file_contents=uploaded_respondents_file.read())
        except xlrd.XLRDError:
            raise forms.ValidationError(
                _('Invalid file format. It must be an excel file with a sheet called respondents.')
            )
        try:
            sheet = book.sheet_by_name('respondents')
        except xlrd.XLRDError:
            raise forms.ValidationError(_('The file must have sheet called respondents'))

        uploaded_respondents = []
        for row_index in range(1, sheet.nrows):
            row = sheet.row_values(row_index)
            # TODO: populate more respondent fields?
            uploaded_respondent = {'email': row[0], 'hierarchy_level': row[1]}
            uploaded_respondents.append(uploaded_respondent)

        return uploaded_respondents

    def save_respondent(self, uploaded_respondent):
        hierarchy_level = HierarchyLevel.objects.filter(name=uploaded_respondent['hierarchy_level']).first()
        respondent = Respondent.objects.filter(email=uploaded_respondent['email']).first()
        user = User.objects.filter(email=uploaded_respondent['email']).first()
        if not respondent:
            respondent = Respondent(
                survey=uploaded_respondent['survey'],
                creator=uploaded_respondent['creator'],
                email=uploaded_respondent['email'],
            )
        if hierarchy_level:
            # TODO: use survey default respondent hierarchy level
            respondent.hierarchy_level = hierarchy_level
        if user:
            respondent.user = user
        respondent.save()

        return respondent

    def save_respondents(self):

        # obtain respondents creator
        creator_pk = self.cleaned_data.get('respondents_creator')
        creator = User.objects.get(pk=creator_pk)

        respondents_data = self.cleaned_data.get('respondents_file', [])
        if respondents_data:
            for respondent_data in respondents_data:
                respondent_data['creator'] = creator
                respondent_data['survey'] = self.instance
                self.save_respondent(respondent_data)
            return
        else:
            return

    def save(self, commit=True):
        survey = super().save(commit=commit)

        self.save_respondents()

        return survey

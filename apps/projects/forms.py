from django import forms
from django.conf import settings
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

import xlrd
from django_select2.forms import Select2MultipleWidget
from treelib import Tree

from .models import Project


class ProjectCreateForm(ModelForm):
    """
    Project create form
    """

    hierarchy_file_help_text = _(
        'You will issue one or more surveys to actors in the system encompassed '
        'by this project. In order to be able to aggregate results well, '
        'please upload the dataflow hierarchy. '
        '<a href="%(template_url)s" download>Click here for data flow hierarchy template</a>.'
    ) % {'template_url': settings.STATIC_URL + 'files/templates/data-flow-hierarchy.xlsx'}

    hierarchy_file = forms.FileField(
        label=_('Data flow hierarchy'),
    )

    _delimiter = '::'

    class Meta:
        model = Project
        fields = ['name', 'description', 'email', 'countries']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
            'countries': Select2MultipleWidget
        }
        help_texts = {
            'email': _('Please provide an email address of a collegue whom '
                       'can be contacted regarding various issues related to this'
                       ' project.')
        }
        labels = {
            'email': _('Contact information')
        }
        required = ['name', 'description', 'email', 'countries', 'hierarchy_file']

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        self.fields['hierarchy_file'].help_text = self.hierarchy_file_help_text

        _required = getattr(self.Meta, 'required', [])
        for field in _required:
            self.fields[field].required = True

    def clean_hierarchy_file(self):
        """
        Returns hierarch tree and levels from uploaded excel file
        (``{'levels': levels, 'tree': tree}``).
        """
        hierarchy_file = self.cleaned_data['hierarchy_file']
        if not hierarchy_file:
            return None

        try:
            book = xlrd.open_workbook(file_contents=hierarchy_file.read())
        except xlrd.XLRDError:
            raise forms.ValidationError(_('Invalid file format'))
        try:
            sheet = book.sheet_by_name('hierarchy')
        except xlrd.XLRDError:
            raise forms.ValidationError(_('The file must have sheet called hierarchy'))

        levels = sheet.row_values(0)
        nodes = self.get_hierarcy_nodes(sheet)
        tree = self.build_hierarchy_tree(nodes)
        return {'tree': tree, 'levels': levels}

    def get_hierarcy_nodes(self, sheet):
        """
        Parse spread sheet and return a set of all possible nodes.
        """
        nodes = set()
        for i in range(1, sheet.nrows):
            row = sheet.row_values(i)
            for j, x in enumerate(row):
                nodes.add(self._delimiter.join(row[:j+1]))
        return nodes

    def parse_hierarchy_node(self, identifier):
        """
        Parse node string. Returns tuple of node (tag, identifier, parent)
        """
        nodes = identifier.split(self._delimiter)
        if len(nodes) == 1:
            return identifier, identifier, None

        tag = nodes[-1]
        parent = self._delimiter.join(nodes[:-1])
        return tag, identifier, parent

    def build_hierarchy_tree(self, nodes):
        """
        Build hierarchy tree from list of nodes.
        """

        tree = Tree()

        # root node
        tree.create_node('root', 0)

        # create all nodes
        for i in nodes:
            name, id, parent = self.parse_hierarchy_node(i)
            tree.create_node(name, id, parent=0)

        # assign parents
        for i in nodes:
            name, id, parent = self.parse_hierarchy_node(i)
            if parent is not None:
                tree.move_node(id, parent)

        return tree

    def save(self, commit=True):
        project = super().save(commit=commit)

        if commit is False:
            return project

        self.save_hierarchy()
        return project

    def save_hierarchy(self):
        project = self.instance
        creator = self.get_hierarchy_creator()

        hierarchy_data = self.cleaned_data.get('hierarchy_file', {})
        if not hierarchy_data:
            return

        self.pre_save_hierarchy()
        hierarchy_tree = hierarchy_data.get('tree')
        hierarchy_levels = hierarchy_data.get('levels')
        hierarchy_lookup = {}
        if hierarchy_tree:
            for i in hierarchy_tree.expand_tree():
                # skip artificial root node
                if hierarchy_tree[i].is_root():
                    continue

                hierarchy_level = hierarchy_tree.depth(hierarchy_tree[i]) - 1
                hierarchy_lookup[i] = project.hierarchies.create(
                    name=hierarchy_tree[i].tag,
                    parent=hierarchy_lookup.get(hierarchy_tree.parent(i).identifier),
                    creator=creator,
                    level_name=hierarchy_levels[hierarchy_level]
                )

    def get_hierarchy_creator(self):
        return self.instance.creator

    def pre_save_hierarchy(self):
        pass


class ProjectUpdateForm(ProjectCreateForm):
    """
    Project update form
    """

    hierarchy_file = forms.FileField(
        label=_('Data flow hierarchy'),
        required=False
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'email', 'countries']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
            'countries': Select2MultipleWidget
        }
        required = ['name', 'description', 'email', 'countries']

    def get_hierarchy_creator(self):
        return self.user

    def pre_save_hierarchy(self):
        """Clear the hierarchy"""
        self.instance.hierarchies.all().delete()

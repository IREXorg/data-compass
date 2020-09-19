from django.utils.translation import pgettext_lazy

from apps.surveys.forms import RoleCreateForm as BaseRoleCreateForm
from apps.surveys.models import Role


class RoleCreateForm(BaseRoleCreateForm):

    class Meta:
        model = Role
        fields = ['name', 'hierarchy_level']
        labels = {
            'hierarchy_level': pgettext_lazy('administrative', 'Level')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hierarchy_level'].required = False

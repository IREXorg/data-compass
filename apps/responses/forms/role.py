from django.utils.translation import ugettext_lazy as _

from apps.surveys.forms import RoleCreateForm as BaseRoleCreateForm
from apps.surveys.models import Role


class RoleCreateForm(BaseRoleCreateForm):

    class Meta:
        model = Role
        fields = ['name', 'hierarchy_level']
        labels = {
            'hierarchy_level': _('Level')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hierarchy_level'].required = False

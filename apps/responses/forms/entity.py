from django.utils.translation import pgettext_lazy

from apps.surveys.forms import EntityCreateForm as BaseEntityCreateForm
from apps.surveys.models import Entity


class EntityCreateForm(BaseEntityCreateForm):

    class Meta:
        model = Entity
        fields = ['name', 'hierarchy_level']
        labels = {
            'hierarchy_level': pgettext_lazy('administrative', 'Level')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hierarchy_level'].required = False

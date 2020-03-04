from django import forms
from django.contrib.postgres.fields import ArrayField
from django.forms import SelectMultiple


class ArraySelectMultiple(SelectMultiple):
    def value_omitted_from_data(self, data, files, name):
        return False


class ChoiceArrayField(ArrayField):
    """
    A field that allows us to store an array of choices.

    Uses Django 1.9's postgres ArrayField
    and a MultipleChoiceField for its formfield.
    """
    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.TypedMultipleChoiceField,
            'choices': self.base_field.choices,
            'coerce': self.base_field.to_python,
            'widget': ArraySelectMultiple
        }

        defaults.update(kwargs)
        return super(ArrayField, self).formfield(**defaults)

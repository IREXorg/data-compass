from django import forms
from django.contrib.auth import get_user_model


class ProfileForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ['avatar', 'first_name', 'last_name', 'email', 'phone_number',
                  'gender', 'country', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
        }

# Generated by Django 3.0.3 on 2020-03-23 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='allow_respondent_roles',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='If Yes, respondents will be able to add their own roles.', verbose_name='allow respondent roles'),
        ),
    ]

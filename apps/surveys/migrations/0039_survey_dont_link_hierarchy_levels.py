# Generated by Django 3.0.3 on 2020-03-17 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0038_add_survey_genders'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='dont_link_hierarchy_levels',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='This can be easier in some contexts, but will limit aggregate or comparative analyses.', verbose_name='do not link respondents with system hierarchy levels'),
        ),
    ]
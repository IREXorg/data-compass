# Generated by Django 3.0.3 on 2020-03-17 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0039_survey_dont_link_hierarchy_levels'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='allow_respondent_hierarchy_levels',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text="Respondents will select from the List you provided for each level. If they can't find theirs, they can add their own?", verbose_name='allow respondent hierarchy levels'),
        ),
    ]

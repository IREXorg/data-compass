# Generated by Django 3.0.3 on 2020-03-17 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0045_alter_login_required_help_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='allow_respondent_datasets',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], default=False, help_text='If Yes, respondents will be able to add their own datasets. This is not recommended.', verbose_name='allow respondent datasets'),
        ),
    ]

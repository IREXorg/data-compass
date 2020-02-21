# Generated by Django 3.0.3 on 2020-02-18 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0016_add_modify_response_related_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='invitation_required',
            field=models.BooleanField(blank=True, default=True, help_text='Do you want the survey to be taken by invited users only?', verbose_name='invitation required'),
        ),
    ]

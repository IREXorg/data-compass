# Generated by Django 3.0.3 on 2020-03-22 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0059_remove_survey_code_unique_constrain'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='allow_collect_email',
            field=models.BooleanField(default=True, verbose_name='collect email address'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='allow_collect_gender',
            field=models.BooleanField(default=True, verbose_name='collect gender'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='allow_collect_name',
            field=models.BooleanField(default=True, verbose_name='collect name'),
        ),
    ]

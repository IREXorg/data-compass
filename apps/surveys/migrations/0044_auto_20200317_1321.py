# Generated by Django 3.0.3 on 2020-03-17 10:21

import core.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0043_auto_20200317_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='languages',
            field=core.fields.ChoiceArrayField(base_field=models.CharField(choices=[('en', 'English'), ('sw', 'Swahili')], max_length=5), help_text='By default, all surveys have an English version. If your survey will be in other languages, select or add them here. You will provide translations later.', size=None, verbose_name='languages'),
        ),
    ]
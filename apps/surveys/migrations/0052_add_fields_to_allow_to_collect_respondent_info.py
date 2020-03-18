# Generated by Django 3.0.3 on 2020-03-18 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0051_remove_field_hierachy_from_entity'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='allow_collect_email',
            field=models.BooleanField(default=True, verbose_name='email address'),
        ),
        migrations.AddField(
            model_name='survey',
            name='allow_collect_gender',
            field=models.BooleanField(default=True, verbose_name='gender'),
        ),
        migrations.AddField(
            model_name='survey',
            name='allow_collect_name',
            field=models.BooleanField(default=True, verbose_name='name'),
        ),
    ]

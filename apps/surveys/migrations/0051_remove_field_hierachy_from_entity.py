# Generated by Django 3.0.3 on 2020-03-18 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0050_add_field_hierachy_level_to_entity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entity',
            name='hierarchy',
        ),
    ]
# Generated by Django 3.0.3 on 2020-03-19 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0055_add_ordering_on_dataset_access_frequency_and_storage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survey',
            name='default_hierarchy',
        ),
    ]

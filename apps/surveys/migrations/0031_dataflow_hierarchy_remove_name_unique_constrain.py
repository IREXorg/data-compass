# Generated by Django 3.0.3 on 2020-03-02 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0030_add_project_entity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataflowhierarchy',
            name='name',
            field=models.CharField(max_length=128, verbose_name='name'),
        ),
    ]

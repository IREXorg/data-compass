# Generated by Django 3.0.3 on 2020-03-11 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_allow_countries_choices_on_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='project',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, db_index=True, verbose_name='modified at'),
        ),
    ]
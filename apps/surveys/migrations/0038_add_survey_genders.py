# Generated by Django 3.0.3 on 2020-03-13 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_add_gender_is_primary'),
        ('surveys', '0037_add_hierarchy_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='genders',
            field=models.ManyToManyField(blank=True, related_name='surveys', related_query_name='survey', to='users.Gender', verbose_name='genders'),
        ),
    ]
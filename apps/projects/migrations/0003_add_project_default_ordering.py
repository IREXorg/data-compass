# Generated by Django 3.0.3 on 2020-02-23 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_project_add_organization_related_query_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['created_at'], 'verbose_name': 'Project', 'verbose_name_plural': 'Projects'},
        ),
    ]

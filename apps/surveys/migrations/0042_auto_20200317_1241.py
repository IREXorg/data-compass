# Generated by Django 3.0.3 on 2020-03-17 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0041_survey_default_hierarchy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='default_hierarchy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='default_hierarchies', related_query_name='default_hierarchy', to='surveys.DataflowHierarchy', verbose_name='default hierarchy'),
        ),
    ]

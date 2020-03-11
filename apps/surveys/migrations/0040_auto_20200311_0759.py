# Generated by Django 3.0.3 on 2020-03-11 04:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0039_entity_survey'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='survey',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='roles', related_query_name='role', to='surveys.Survey', verbose_name='survey'),
        ),
        migrations.AlterField(
            model_name='entity',
            name='hierarchy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entities', related_query_name='entity', to='surveys.DataflowHierarchy', verbose_name='hierarchy'),
        ),
    ]

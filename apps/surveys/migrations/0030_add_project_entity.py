# Generated by Django 3.0.3 on 2020-02-24 21:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_add_project_facilitators'),
        ('surveys', '0029_response_completed_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entities', related_query_name='entity', to='projects.Project', verbose_name='project'),
        ),
        migrations.AlterField(
            model_name='entity',
            name='hierarchy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entities', related_query_name='entity', to='surveys.DataflowHierarchy', verbose_name='hierarchy'),
        ),
    ]

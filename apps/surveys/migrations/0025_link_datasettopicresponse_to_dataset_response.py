# Generated by Django 3.0.3 on 2020-02-22 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0024_add_survey_default_ordering'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datasettopicresponse',
            name='dataset',
        ),
        migrations.RemoveField(
            model_name='datasettopicresponse',
            name='response',
        ),
        migrations.AddField(
            model_name='datasettopicresponse',
            name='dataset_response',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topic_responses', related_query_name='topic_response', to='surveys.DatasetResponse', verbose_name='dataset response'),
            preserve_default=False,
        ),
    ]
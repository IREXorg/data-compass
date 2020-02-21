# Generated by Django 3.0.3 on 2020-02-20 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0021_dataset_topics'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='datasets', related_query_name='dataset', to='surveys.Survey', verbose_name='survey'),
            preserve_default=False,
        ),
    ]
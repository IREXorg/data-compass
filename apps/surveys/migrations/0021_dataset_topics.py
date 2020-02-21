# Generated by Django 3.0.3 on 2020-02-20 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0020_response_consented_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='topic',
        ),
        migrations.AddField(
            model_name='dataset',
            name='topics',
            field=models.ManyToManyField(blank=True, related_name='datasets', related_query_name='dataset', to='surveys.Topic', verbose_name='topics'),
        ),
    ]
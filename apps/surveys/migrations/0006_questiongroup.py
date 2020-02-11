# Generated by Django 3.0.3 on 2020-02-11 16:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('surveys', '0005_dataset'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='name')),
                ('group_number', models.IntegerField(blank=True, null=True, verbose_name='group number')),
                ('creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_question_groups', related_query_name='created_question_group', to=settings.AUTH_USER_MODEL, verbose_name='creator')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_groups', related_query_name='question_group', to='surveys.Survey', verbose_name='survey')),
            ],
            options={
                'verbose_name': 'Question Group',
                'verbose_name_plural': 'Question Groups',
                'unique_together': {('survey', 'group_number')},
            },
        ),
    ]

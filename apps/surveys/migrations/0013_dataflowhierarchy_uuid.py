# Generated by Django 3.0.3 on 2020-02-11 19:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0012_questionresponse'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataflowhierarchy',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID'),
        ),
    ]
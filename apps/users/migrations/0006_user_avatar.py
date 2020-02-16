# Generated by Django 3.0.3 on 2020-02-12 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_is_respondent'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='users/avatars', verbose_name='avatar'),
        ),
    ]
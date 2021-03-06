# Generated by Django 3.0.5 on 2020-05-06 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maze', '0003_auto_20200506_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='apikeys',
            name='last_login',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='最終アクセス時刻'),
        ),
        migrations.AddField(
            model_name='practicehistory',
            name='action_date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='操作時刻'),
        ),
    ]

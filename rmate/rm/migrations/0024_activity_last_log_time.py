# Generated by Django 4.1.5 on 2023-03-23 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rm', '0023_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='last_log_time',
            field=models.CharField(max_length=100, null=True),
        ),
    ]

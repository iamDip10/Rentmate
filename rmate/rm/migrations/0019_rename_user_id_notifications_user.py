# Generated by Django 4.1.5 on 2023-02-09 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rm', '0018_notifications'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notifications',
            old_name='user_id',
            new_name='user',
        ),
    ]
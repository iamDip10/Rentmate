# Generated by Django 4.1.5 on 2023-03-23 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rm', '0021_residant_authheticate'),
    ]

    operations = [
        migrations.AddField(
            model_name='residant',
            name='OTP',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
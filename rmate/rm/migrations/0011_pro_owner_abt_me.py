# Generated by Django 4.1.5 on 2023-04-29 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rm', '0010_alter_pro_owner_twofact'),
    ]

    operations = [
        migrations.AddField(
            model_name='pro_owner',
            name='abt_me',
            field=models.CharField(max_length=800, null=True),
        ),
    ]
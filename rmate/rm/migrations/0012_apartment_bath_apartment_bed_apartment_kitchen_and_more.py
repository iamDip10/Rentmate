# Generated by Django 4.1.5 on 2023-04-30 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rm', '0011_pro_owner_abt_me'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='bath',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='apartment',
            name='bed',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='apartment',
            name='kitchen',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='apartment',
            name='living',
            field=models.CharField(max_length=10, null=True),
        ),
    ]

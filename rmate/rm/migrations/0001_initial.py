# Generated by Django 4.1.5 on 2023-04-26 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='apartment',
            fields=[
                ('id', models.CharField(max_length=60, primary_key=True, serialize=False)),
                ('occupy', models.CharField(default='NO', max_length=4)),
            ],
            options={
                'db_table': 'apartments',
            },
        ),
        migrations.CreateModel(
            name='Pro_owner',
            fields=[
                ('fname', models.CharField(max_length=10)),
                ('lname', models.CharField(max_length=10)),
                ('gender', models.CharField(max_length=8)),
                ('number', models.CharField(default='', max_length=12, primary_key=True, serialize=False)),
                ('mail', models.CharField(max_length=100)),
                ('psword', models.CharField(max_length=40)),
                ('p_addrs', models.CharField(max_length=200)),
                ('div', models.CharField(max_length=10)),
                ('area', models.CharField(max_length=10)),
                ('nid', models.CharField(max_length=20)),
                ('hid', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'pro_owner',
            },
        ),
        migrations.CreateModel(
            name='Residant',
            fields=[
                ('fname', models.CharField(max_length=10)),
                ('lname', models.CharField(max_length=10)),
                ('gender', models.CharField(max_length=8)),
                ('phn', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('mail', models.CharField(max_length=100)),
                ('psword', models.CharField(max_length=40)),
                ('p_addrs', models.CharField(max_length=200)),
                ('div', models.CharField(max_length=10)),
                ('area', models.CharField(max_length=10)),
                ('nid', models.CharField(max_length=20)),
                ('uname', models.CharField(max_length=30, null=True)),
                ('per_addrs', models.CharField(max_length=100, null=True)),
                ('about_me', models.CharField(max_length=500, null=True)),
                ('authheticate', models.CharField(default='NO', max_length=500)),
                ('OTP', models.CharField(max_length=100, null=True)),
                ('image', models.ImageField(null=True, upload_to='img/')),
                ('apps', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rm.apartment')),
                ('hown', models.ForeignKey(default='H123', on_delete=django.db.models.deletion.CASCADE, to='rm.pro_owner')),
            ],
            options={
                'db_table': 'residant',
            },
        ),
        migrations.CreateModel(
            name='ResRent',
            fields=[
                ('amount', models.IntegerField(default=0, null=True)),
                ('status', models.CharField(default='NOT PAID', max_length=30, null=True)),
                ('deadline', models.CharField(default='none', max_length=40, null=True)),
                ('month', models.CharField(default='none', max_length=30, null=True)),
                ('paymentID', models.CharField(default='none', max_length=100)),
                ('date', models.CharField(default='0-0-0000', max_length=50, null=True)),
                ('uniqID', models.CharField(max_length=60, primary_key=True, serialize=False)),
                ('year', models.CharField(max_length=40, null=True)),
                ('apps', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rm.apartment')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rm.pro_owner')),
                ('user', models.ForeignKey(default='NULL', on_delete=django.db.models.deletion.CASCADE, to='rm.residant')),
            ],
            options={
                'db_table': 'residantrent',
            },
        ),
        migrations.CreateModel(
            name='rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.CharField(default='0', max_length=100)),
                ('commnt', models.CharField(default='', max_length=300, null=True)),
                ('owner', models.ForeignKey(default='NULL', on_delete=django.db.models.deletion.CASCADE, to='rm.pro_owner')),
                ('residnt', models.ForeignKey(default='NULL', on_delete=django.db.models.deletion.CASCADE, to='rm.residant')),
            ],
            options={
                'db_table': 'ratting',
            },
        ),
        migrations.CreateModel(
            name='otherActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activ_time', models.CharField(max_length=100, null=True)),
                ('msg', models.CharField(max_length=140, null=True)),
                ('user', models.ForeignKey(default='NULL', on_delete=django.db.models.deletion.CASCADE, to='rm.residant')),
            ],
            options={
                'db_table': 'otherActivity',
            },
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification', models.CharField(default=' ', max_length=400, null=True)),
                ('date', models.CharField(default=' ', max_length=30, null=True)),
                ('status', models.CharField(default='unread', max_length=60)),
                ('user', models.ForeignKey(default='NULL', on_delete=django.db.models.deletion.CASCADE, to='rm.residant')),
            ],
            options={
                'db_table': 'notifications',
            },
        ),
        migrations.CreateModel(
            name='Complain',
            fields=[
                ('date', models.CharField(max_length=30)),
                ('comID', models.AutoField(primary_key=True, serialize=False)),
                ('slv_status', models.CharField(default='Not Solved', max_length=20)),
                ('prob_type', models.CharField(max_length=50)),
                ('prob_desc', models.CharField(max_length=200)),
                ('nei_ID', models.CharField(max_length=50, null=True)),
                ('year', models.CharField(default='0', max_length=7)),
                ('app', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rm.apartment')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rm.pro_owner')),
                ('user', models.ForeignKey(default='NULL', on_delete=django.db.models.deletion.CASCADE, to='rm.residant')),
            ],
            options={
                'db_table': 'complain',
            },
        ),
        migrations.AddField(
            model_name='apartment',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rm.pro_owner'),
        ),
        migrations.CreateModel(
            name='activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active_time', models.IntegerField(null=True)),
                ('last_login', models.CharField(max_length=100, null=True)),
                ('side_activity', models.CharField(max_length=150, null=True)),
                ('last_log_time', models.CharField(max_length=100, null=True)),
                ('user', models.ForeignKey(default='NULL', on_delete=django.db.models.deletion.CASCADE, to='rm.residant')),
            ],
            options={
                'db_table': 'activity',
            },
        ),
    ]
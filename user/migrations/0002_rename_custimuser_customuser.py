# Generated by Django 5.1.7 on 2025-03-27 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustimUser',
            new_name='CustomUser',
        ),
    ]

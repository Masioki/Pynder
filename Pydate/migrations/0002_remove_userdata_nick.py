# Generated by Django 3.0.5 on 2020-05-09 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Pydate', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdata',
            name='nick',
        ),
    ]
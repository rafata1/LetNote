# Generated by Django 3.1.6 on 2021-02-17 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('note_system', '0007_auto_20210217_1311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='noteitem',
            name='created_at',
        ),
    ]

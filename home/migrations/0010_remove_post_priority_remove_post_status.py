# Generated by Django 4.2.7 on 2023-12-07 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_post_priority_post_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='priority',
        ),
        migrations.RemoveField(
            model_name='post',
            name='status',
        ),
    ]

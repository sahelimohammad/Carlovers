# Generated by Django 4.2.7 on 2023-12-07 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_dislike_delete_unvote'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='home/%Y/%m/%d/'),
        ),
    ]

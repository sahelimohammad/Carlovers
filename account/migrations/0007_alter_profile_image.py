# Generated by Django 4.2.7 on 2023-12-07 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='account/%Y/%m/%d/'),
        ),
    ]
# Generated by Django 4.1.3 on 2022-12-22 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aws', '0004_accountconfiguration_is_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountconfiguration',
            name='is_default',
            field=models.BooleanField(default=True),
        ),
    ]

# Generated by Django 5.2 on 2025-04-16 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medcenter', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ['last_name'], 'verbose_name': 'Человек', 'verbose_name_plural': 'Люди'},
        ),
    ]

# Generated by Django 5.0.6 on 2024-09-16 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='rating',
            new_name='ratings',
        ),
    ]

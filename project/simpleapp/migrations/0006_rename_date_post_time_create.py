# Generated by Django 5.0.2 on 2024-03-06 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simpleapp', '0005_alter_post_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='date',
            new_name='time_create',
        ),
    ]
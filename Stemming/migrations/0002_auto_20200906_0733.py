# Generated by Django 2.2 on 2020-09-06 00:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Stemming', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='message',
            new_name='comment',
        ),
        migrations.RenameField(
            model_name='contact',
            old_name='first_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='email',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='last_name',
        ),
    ]

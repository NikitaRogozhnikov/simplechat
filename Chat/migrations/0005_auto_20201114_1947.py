# Generated by Django 3.1.3 on 2020-11-14 16:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Chat', '0004_chat_chat_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='chat_name',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='type',
        ),
    ]

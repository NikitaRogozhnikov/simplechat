# Generated by Django 3.1.3 on 2020-11-14 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Chat', '0003_remove_message_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='chat_name',
            field=models.CharField(default=1, max_length=30, verbose_name='Имя чата'),
            preserve_default=False,
        ),
    ]

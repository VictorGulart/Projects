# Generated by Django 3.1.4 on 2020-12-14 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0002_auto_20201213_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='message',
            field=models.TextField(default='Add Notes'),
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(default='Add Title', max_length=200),
        ),
    ]

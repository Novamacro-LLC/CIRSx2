# Generated by Django 5.0 on 2024-09-17 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0004_alter_shoeyawards_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoeyawards',
            name='year',
            field=models.IntegerField(default=0),
        ),
    ]
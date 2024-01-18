# Generated by Django 5.0 on 2024-01-15 22:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_currations_document_curr_num'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cur_name', models.CharField(max_length=100)),
                ('cat_name', models.CharField(max_length=100)),
                ('subcat_name', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='document',
            name='curr_num',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='library.curations'),
        ),
        migrations.DeleteModel(
            name='Currations',
        ),
    ]
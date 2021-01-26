# Generated by Django 2.1.7 on 2021-01-23 17:38

import ckeditor_uploader.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BroadCast_Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('message', ckeditor_uploader.fields.RichTextUploadingField()),
            ],
            options={
                'verbose_name': 'BroadCast Email to all Member',
                'verbose_name_plural': 'BroadCast Email',
            },
        ),
    ]
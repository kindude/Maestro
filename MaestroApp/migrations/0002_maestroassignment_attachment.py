# Generated by Django 5.1.5 on 2025-03-12 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MaestroApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='maestroassignment',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='assignments/'),
        ),
    ]

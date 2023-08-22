# Generated by Django 3.2.20 on 2023-08-22 09:32

from django.db import migrations, models
from django.utils import timezone

class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20230822_0929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='updated',
            field=models.DateTimeField(auto_now=True, default=timezone.now),
        ),
    ]
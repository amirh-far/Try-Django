# Generated by Django 3.2.20 on 2023-08-22 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_alter_article_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

# Generated by Django 3.2.25 on 2024-12-06 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_newsletter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='subject',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

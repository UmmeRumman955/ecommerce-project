# Generated by Django 5.1.4 on 2024-12-31 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_productitem_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productitem',
            name='slug',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

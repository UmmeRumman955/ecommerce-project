# Generated by Django 5.1.4 on 2025-01-02 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_productitem_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='slug',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

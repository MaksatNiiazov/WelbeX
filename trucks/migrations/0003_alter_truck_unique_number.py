# Generated by Django 5.0.3 on 2024-03-24 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trucks', '0002_alter_truck_capacity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='truck',
            name='unique_number',
            field=models.CharField(max_length=5, unique=True),
        ),
    ]

# Generated by Django 5.0.3 on 2024-03-24 06:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_number', models.CharField(editable=False, max_length=5, unique=True)),
                ('capacity', models.PositiveIntegerField(help_text='Capacity in kilograms.')),
                ('current_spot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trucks', to='location.spot')),
            ],
        ),
    ]
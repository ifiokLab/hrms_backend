# Generated by Django 4.1.6 on 2024-01-21 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0005_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='App.department'),
        ),
    ]

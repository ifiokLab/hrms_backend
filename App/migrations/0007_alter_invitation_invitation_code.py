# Generated by Django 4.1.6 on 2024-01-21 15:41

import App.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0006_alter_invitation_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='invitation_code',
            field=models.CharField(default=App.models.generate_invitation_code, max_length=50, unique=True),
        ),
    ]

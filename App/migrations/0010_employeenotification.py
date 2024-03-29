# Generated by Django 4.1.6 on 2024-01-23 12:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0009_membership_date_joined_membership_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Suspended', 'Suspended'), ('Inactive', 'Inctive')], default='Active', max_length=10)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('reason', models.TextField()),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.organization')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 4.1.6 on 2024-01-24 12:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0010_employeenotification'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=100)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField()),
                ('hours_worked', models.DecimalField(decimal_places=2, max_digits=5)),
                ('activity_description', models.TextField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Under Review', 'Under Review'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=20)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.organization')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payroll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('hourly_rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('salary_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.organization')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_schedule', models.CharField(choices=[('Monthly', 'Monthly'), ('Bi-Weekly', 'Bi-Weekly'), ('Weekly', 'Weekly')], default='Monthly', max_length=20)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.organization')),
            ],
        ),
    ]

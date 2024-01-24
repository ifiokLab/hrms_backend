from django.db import models
from django.conf import settings
from .manager import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings
# Create your models here.


class myuser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=40,blank=False)
    last_name = models.CharField(max_length=40,blank=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_employer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name',]
    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'



class Department(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Organization(models.Model):
    name = models.CharField(max_length=100)
    overview = models.TextField(blank=True,null=True)
    logo = models.ImageField(upload_to='org-logo/',blank=True,null=True)
    employer =  models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    employees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='employees',blank=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
    ]

    DEPARTMENT_CHOICES = [
        ('IT', 'Information Technology'),
        ('HR', 'Human Resources'),
        ('FIN', 'Finance'),
        ('SALES', 'Sales'),
        ('MKT', 'Marketing'),
        ('ENG', 'Engineering'),
        ('OPS', 'Operations'),
        ('ADMIN', 'Administration'),
        ('SUPPORT', 'Customer Support'),
        ('LEGAL', 'Legal'),
        ('QA', 'Quality Assurance'),
        ('RD', 'Research and Development'),
        ('PR', 'Public Relations'),
        ('LOG', 'Logistics'),
        # Add more choices as needed
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    #department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES, default='IT')
    date_of_birth = models.DateField(blank=True,null= True)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES,blank=True,null=True)
    marital_status = models.CharField(max_length=100, choices=MARITAL_STATUS_CHOICES,blank=True,null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='Profile/',blank=True,null=True)
    #organizations = models.ManyToManyField(Organization)
    # Other fields

    def __str__(self):
        return self.user


class Membership(models.Model):
    STATUS = [
        ('Active', 'Active'),
        ('Suspended', 'Suspended'),
        ('Inactive', 'Inctive'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default='Active')
    date_joined = models.DateTimeField(auto_now_add=True,null=True)

class Employer(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
    ]

    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True,null= True)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES,blank=True,null=True)
    marital_status = models.CharField(max_length=100, choices=MARITAL_STATUS_CHOICES,blank=True,null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='Profile/',blank=True,null=True)
    # Other fields

    def __str__(self):
        return self.user

from django.utils.crypto import get_random_string
def generate_invitation_code():
    return get_random_string(12)

class Invitation(models.Model):
    
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invitations_sent')
    invited_user = models.EmailField(unique=True)
    organization =  models.ForeignKey(Organization,on_delete=models.CASCADE,null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    invitation_code = models.CharField(max_length=50, default=generate_invitation_code, unique=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Invitation from {self.invited_by.email} to {self.invited_user}"



class EmployeeNotification(models.Model):
    STATUS = [
        ('Active', 'Active'),
        ('Suspended', 'Suspended'),
        ('Inactive', 'Inctive'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS, default='Active')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True)
    reason = models.TextField()


class TimeSheet(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Under Review', 'Under Review'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=100)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)
    activity_description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    def formatted_start_date(self):
        return self.start_date.strftime('%Y-%m-%d %H:%M:%S')

    def formatted_end_date(self):
        return self.end_date.strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self):
        return f"{self.user.first_name}'s TimeSheet - {self.start_date}"


class Payroll(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True) 
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    salary_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
  

class PaymentSchedule(models.Model):
    PAYMENT_SCHEDULE_CHOICES = [
        ('Monthly', 'Monthly'),
        ('Bi-Weekly', 'Bi-Weekly'),
        ('Weekly', 'Weekly'),
    ]

    payment_schedule = models.CharField(max_length=20,choices=PAYMENT_SCHEDULE_CHOICES,default='Monthly')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.organization.name}"
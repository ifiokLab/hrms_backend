from rest_framework import serializers
from .models import *

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = myuser
        fields = ('id', 'email', 'first_name', 'last_name',)


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('name', 'logo', 'overview',)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ('invited_user', 'organization', 'department',)

    
class TimeSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSheet
        fields = ['organization','task_name','end_date','hours_worked','activity_description']
from django.shortcuts import render, redirect,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import stripe
from django.conf import settings  
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser
# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models import F,Q, ExpressionWrapper
# Create your views here.
from decimal import Decimal,ROUND_HALF_UP






class EmployerSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = MyUserSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            
            user = serializer.save()
            user.set_password(request.data.get('password'))
            user.is_employer = True
            user.save()
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            user_data = {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'isLoggedIn':'true',
                'auth_token': token.key, 
                'isEmployer': user.is_employer,
            }
            return Response({'success': True, 'message': 'Signup successful', 'user': user_data}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'message': 'Signup failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




class EmployerLoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user.is_employer:
            print(request.data)
            login(request, user)
            serializer = MyUserSerializer(user)

            #return Response(serializer.data)
            token, created = Token.objects.get_or_create(user=user)
            
            user_data = {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name, 
                'isLoggedIn':'true',
                'auth_token': token.key, 
                'isEmployer': user.is_employer,
            }
            print(user_data)
          
            return Response({'success': True, 'message': 'Login successful', 'user': user_data},status=status.HTTP_201_CREATED)
        else:
            return Response({'success': False, 'error': 'Invalid credentials'}, status=401)




class OrganizationCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    
    def post(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
       
        print(request.data)
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employer=user)  # Set the instructor to the current user
            return Response({'success': True, },status=status.HTTP_201_CREATED)
       
        return Response({'success': False,'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class EmployerOrganizationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        organizations = Organization.objects.filter(employer = user)
        
        all_organizations = []
        for data in organizations:
            org_data = {
                'id': data.id,
                'employer': f"{data.employer.first_name} {data.employer.last_name}",
                'name': data.name,
                'overview': data.overview,
                'logo': data.logo.url,
                'employee_count': data.employees.count(),
                
    
            }
            all_organizations.append(org_data)#
        print(all_organizations)
       
        return Response({'all_organizations':all_organizations}, status=status.HTTP_200_OK)



class OrganizationEditView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request,pk, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        organization = Organization.objects.get(id = pk,employer = user)
        
        org_data = {
            'id': organization.id,
            'employer': f"{organization.employer.first_name} {organization.employer.last_name}",
            'name': organization.name,
            'overview': organization.overview,
            'logo': organization.logo.name,
            'employee_count': organization.employees.count(),    
    
        }
        print(org_data)
       
        return Response(org_data, status=status.HTTP_200_OK)

    def put(self, request,pk,*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        # Retrieve the organization based on the user making the request
        print(request.data)
        organization = Organization.objects.get(id = pk,employer = user)
        serializer = OrganizationSerializer(organization, data=request.data)
        if serializer.is_valid():
            serializer.save()
            #return Response(serializer.data)
            return Response({'success': True, },status=status.HTTP_201_CREATED)
       
        return Response({'success': False,'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class OrganizationDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, pk, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        try:
            # Retrieve the organization based on the user making the request
            organization = Organization.objects.get(id=pk, employer=user)
        except Organization.DoesNotExist:
            return Response({"message": "Organization not found."}, status=status.HTTP_404_NOT_FOUND)

        organization.delete()
        return Response({'success': True, "detail": "Organization deleted successfully."},status=status.HTTP_201_CREATED)
     

    

class DepartmentListView(APIView):
    def get(self, request, *args, **kwargs):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


"""class InvitationCreateView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        #organization = Organization.objects.get(id = data.organizationId)
        #print(organization)
        serializer = InvitationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(invited_by = user)
            # Perform any additional actions (e.g., sending an email with the invitation code)
            return Response({'success': True}, status=status.HTTP_201_CREATED)

        return Response({'success': False,'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
"""
from django.core.mail import send_mail
class InvitationCreateView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user

        serializer = InvitationSerializer(data=request.data)
        if serializer.is_valid():
            invitation = serializer.save(invited_by=user)
           
            registration_link = f'http://localhost:3000/employee-signup/{invitation.invitation_code}/'
            # Send email with the invitation code
            subject = 'Invitation to join our organization'
            message = f'You are invited to join our organization. Click the link below to register:\n\n{registration_link}'
            from_email = 'your@example.com'  # Replace with your email
            recipient_list = [invitation.invited_user]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return Response({'success': True}, status=status.HTTP_201_CREATED)

        return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



    
class RegisterViaLinkView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, invitation_code, format=None):
        if Invitation.objects.filter(invitation_code=invitation_code, is_accepted=True).exists():
            return Response({'success':False,'message':'Expired or invalid invitation link.'}, status=status.HTTP_201_CREATED)
        else:          

            invitation = get_object_or_404(Invitation, invitation_code=invitation_code, is_accepted=False)

            serializer = MyUserSerializer(data=request.data)
            if serializer.is_valid():
                print(request.data)
                user = serializer.save()
                user.is_employee = True
                #user.department = invitation.invited_by.department
                user.save()
                organization = Organization.objects.get(id = invitation.organization.id)
                organization.employees.add(user)
                # Mark the invitation as accepted
                invitation.is_accepted = True
                invitation.save()
                Membership.objects.create(
                    user = user,
                    organization = organization,
                    department = invitation.department
                )

                response_data = {
                    'message': 'Registration successful! You have joined the organization.',
                    'user': serializer.data,
                    'success':True,
                }

                return Response(response_data, status=status.HTTP_201_CREATED)

            return Response({'message':serializer.errors,'success':False}, status=status.HTTP_400_BAD_REQUEST)




class OrganizationDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request,Id, *args, **kwargs):

        
        organization = Organization.objects.get(id = Id)
        org_data = {
            'id': organization .id,
            'employer': f"{organization.employer.first_name} {organization.employer.last_name}",
            'name': organization.name,
            'overview': organization.overview,
            'logo': organization.logo.url,
            'employee_count': organization.employees.count(),
            

        }
        print(org_data)
       
        return Response(org_data, status=status.HTTP_200_OK)


class EmployeeListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request,Id, *args, **kwargs):
       
        membership = Membership.objects.filter(organization__id = Id)
        
        all_members = []
        for data in membership:
            org_data = {
                'id': data.id,
                'first_name': data.user.first_name,
                'last_name':data.user.last_name,
                'department':data.department.title, 
                'organization':data.organization.name, 
                'status':data.status, 

    
            }
            all_members.append(org_data)#
        print(all_members)
       
        return Response(all_members, status=status.HTTP_200_OK)




class EmployeeDepartmentChangeView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    def put(self, request,pk,*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        department = Department.objects.get(id = request.data['department'])
        # Retrieve the organization based on the user making the request
        if Membership.objects.filter(id = pk).exists():
            membership = Membership.objects.get(id = pk)
            membership.department = department
            membership.save()
           
            return Response({'success': True, },status=status.HTTP_201_CREATED)
       
        return Response({'success': False,'message':'An unknown error occured'}, status=status.HTTP_400_BAD_REQUEST)



class EmployeeRemoveView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    def post(self, request,pk,*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        print(request.data)
        # Retrieve the organization based on the user making the request
        if Membership.objects.filter(id = pk).exists():
            membership = Membership.objects.get(id = pk)
            membership.status = request.data['status']
            membership.save()
            EmployeeNotification.objects.create(
                user = membership.user,
                organization = membership.organization,
                status = membership.status,
                reason = request.data['reason'],
                end_date = request.data['date'],
            )
           
            return Response({'success': True, },status=status.HTTP_201_CREATED)
       
        return Response({'success': False,'message':'An unknown error occured'}, status=status.HTTP_400_BAD_REQUEST)



class EmployeeOffboardingList(APIView):
    permission_classes = [AllowAny]

    def get(self, request,Id, *args, **kwargs):
       
        membership = Membership.objects.filter(organization__id = Id,status = 'Inactive')
        
        all_members = []
        for data in membership:
            org_data = {
                'id': data.id,
                'first_name': data.user.first_name,
                'last_name':data.user.last_name,
                'department':data.department.title, 
                'organization':data.organization.name, 
                'status':data.status, 

    
            }
            all_members.append(org_data)#
        print(all_members)
       
        return Response(all_members, status=status.HTTP_200_OK)


class EmployeeOnboardingList(APIView):
    permission_classes = [AllowAny]

    def get(self, request,Id, *args, **kwargs):
       
        invitation = Invitation.objects.filter(organization__id = Id)
        
        all_members = []
        for data in invitation:
            org_data = {
                'id': data.id,
                'invited_by': f"{data.invited_by.first_name} {data.invited_by.last_name}",
                'department':data.department.title, 
                'organization':data.organization.name, 
                'invited_user':data.invited_user, 
                'status':'Accepted' if data.is_accepted else 'Pending', 

    
            }
            all_members.append(org_data)#
        print(all_members)
       
        return Response(all_members, status=status.HTTP_200_OK)




class CreateTimeSheetAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    def post(self, request, format=None):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        print('request.data:',request.data)
        serializer = TimeSheetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)  # Assuming you're associating the timesheet with the logged-in user
            return Response({'success':True,'data':serializer.data,}, status=status.HTTP_201_CREATED)
        return Response({'success':False,'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




class UserTimeSheet(APIView):
    permission_classes = [AllowAny]

    def get(self, request,Id, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        _, token = auth_header.split()
        # Check if the token is valid
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
       
        timesheet = TimeSheet.objects.filter(organization__id = Id,user = user)
        
        all_timesheet = []
        for data in timesheet:
            org_data = {
                'id': data.id,
                'user': f"{data.user.first_name} {data.user.last_name}",
                'task_name':data.task_name, 
                'organization':data.organization.name, 
                'date':data.formatted_end_date(), 
                'hours_worked':data.hours_worked, 
                'activity_description':data.activity_description, 
                'hours_worked':data.hours_worked, 

    
            }
            all_timesheet.append(org_data)#
        print(all_timesheet)
       
        return Response(all_timesheet, status=status.HTTP_200_OK)


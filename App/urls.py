from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('organization/signup/',views.EmployerSignupView.as_view(), name='organization-signup'),
    path('organization/login/',views.EmployerLoginView.as_view(), name='organization-login'),
    path('organization/create/',views.OrganizationCreateView.as_view(), name='organization-create'),
    path('organization/list/',views.EmployerOrganizationsView.as_view(), name='organization-list'),
    path('organization/<int:pk>/edit/', views.OrganizationEditView.as_view(), name='organization-edit'),
    path('organization/<int:pk>/delete/', views.OrganizationDeleteView.as_view(), name='organization-delete'),
    path('invitation/create/',views.InvitationCreateView.as_view(), name='invitation-create'),
    path('departments/list/',views.DepartmentListView.as_view(), name='departments-list'),
    path('register-via-link/<str:invitation_code>/', views.RegisterViaLinkView.as_view(), name='register_via_link'),
    path('organization/<int:Id>/',views.OrganizationDetailView.as_view(), name='organization-detail'),
    path('employees/list/<int:Id>/',views.EmployeeListView.as_view(), name='employee-list'),
    path('membership-department/<int:pk>/change/',views.EmployeeDepartmentChangeView.as_view(), name='membership-department'),
    path('membership-department/<int:pk>/remove/',views.EmployeeRemoveView.as_view(), name='membership-remove'),
    path('off-boarding-list/<int:Id>/',views.EmployeeOffboardingList.as_view(), name='off-boarding-list'),
    path('on-boarding-list/<int:Id>/',views.EmployeeOnboardingList.as_view(), name='on-boarding-list'),

    path('create-time-sheet/',views.CreateTimeSheetAPIView.as_view(), name='create-time-sheet'),
    path('time-sheet/<int:Id>/list/',views.UserTimeSheet.as_view(), name='time-sheet'),
]
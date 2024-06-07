from django.urls import path

from .views import profile, profile_edit, profile_settings, profile_email_change, profile_email_verify, profile_delete

app_name = 'users'

urlpatterns = [
    path('', profile, name='profile'),
    path('edit/', profile_edit, name='profile_edit'),
    path('onboarding/', profile_edit, name='profile_onboarding'),
    path('settings/', profile_settings, name='profile_settings'),
    path('email/change/', profile_email_change, name='profile_email_change'),
    path('email/verify/', profile_email_verify, name='profile_email_verify'),
    path('delete/', profile_delete, name='profile_delete'),
]

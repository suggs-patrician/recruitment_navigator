from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_step1, name='register'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('complete-registration/', views.complete_registration, name='complete_registration'),
    path('resend-verification/', views.resend_verification, name='resend_verification'),
]
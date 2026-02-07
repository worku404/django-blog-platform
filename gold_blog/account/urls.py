from django.urls import path, include
from . import  views
urlpatterns = [
    path('', include('django.contrib.auth.urls'), name='password_change'),
    path('register/', views.register, name='register'),
    path('verify_email/', views.verify_email, name='verify_email'),
    path("verify_email/resend/", views.resend_otp, name="resend_otp"),
]
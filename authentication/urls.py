"""
Authentication API Urls
"""

# Standard library imports.
from django.urls import path

# Related third party imports.

# Local application/library specific imports.
from . import views

urlpatterns = [
    path('registration/', views.RegistrationAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
]
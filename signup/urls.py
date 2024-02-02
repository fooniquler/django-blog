from django.urls import path, include
from .views import UserRegistrationView, CustomLoginView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
]

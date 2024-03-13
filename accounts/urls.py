from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView, ProfileView, VerificationView
from . import views

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('active/<uidb64>/<token>/', VerificationView.as_view(), name='active'),  # Added trailing slash
]

from django.shortcuts import render, redirect
from .forms import UserRegistrationForm,UserUpdateForm
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView
from django.contrib import messages
from train.models import TrainPurchase, UserReviews
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.views import View


# Create your views here.
class UserRegistrationView(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        user = form.save()
        
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirm_link = f'https://brrailway.onrender.com/accounts/active/{uid}/{token}'
        email_subject = "Confirm Your Email"
        email_body = render_to_string('accounts/confirm_email.html', {'confirm_link': confirm_link})
        send_email = EmailMultiAlternatives(email_subject, '', to=[user.email])
        send_email.attach_alternative(email_body, "text/html")
        send_email.send()

        messages.success(self.request, "Check your email for confirmation.")
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
  
class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated. You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid activation link. Please try again or contact support.')
            return redirect('register') 
    
class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        messages.success(self.request, "Login successfully")
        return reverse_lazy('home')
    
class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            # Redirect authenticated users to the home page
            return reverse_lazy('home')
        else:
            # Redirect unauthenticated users to the login page
            return reverse_lazy('login')

class ProfileView(LoginRequiredMixin, ListView):
    template_name = 'accounts/profile.html'
    balance = 0

    def get(self, request):
        user_purchases = TrainPurchase.objects.filter(user=request.user)
        user_review = UserReviews.objects.filter(user=request.user)
        account_balance = request.user.account.balance

        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {
            'user_purchases': user_purchases,
            'user_review': user_review,
            'account_balance': account_balance,
            'form': form,
        })

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        return render(request, self.template_name, {'form': form})

 
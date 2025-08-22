from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.views import View
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
from .forms import RegistrationForm, LoginForm


class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, "registration/register.html", {"form": form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("accounts:login")
        return render(request, "registration/register.html", {"form": form})


class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'registration/login.html'

    def get_success_url(self):
            return reverse_lazy('home')
    
class CustomLogoutView(LogoutView):
    next_page = '/'  # or reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

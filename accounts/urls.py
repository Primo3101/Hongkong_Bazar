from django.urls import path
from .views import RegisterView, CustomLoginView
from django.contrib.auth.views import LogoutView

app_name = "accounts"

urlpatterns = [
    path("login/", CustomLoginView.as_view(),name="login"),
    path("logout/", LogoutView.as_view(),name="logout"),
    path('register/',RegisterView.as_view(), name='register'),
]
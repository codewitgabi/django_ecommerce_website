from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name= "accounts"
urlpatterns = [
	path("", views.signup, name= "signup"),
	path("login/", auth_views.LoginView.as_view(template_name= "accounts/login.html", extra_context= {"login_error": "Please enter a correct email and password. Note that both fields may be case-sensitive."}), name= "login"),
	path("logout/", auth_views.LogoutView.as_view(next_page= "accounts:signup"), name= "logout"),
]
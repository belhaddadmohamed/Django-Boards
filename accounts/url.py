from sre_constants import SUCCESS
from unicodedata import name
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("login", auth_views.LoginView.as_view(template_name = 'login.html'), name='login'),
    path('setting/change_password/', auth_views.PasswordChangeView.as_view(template_name='change_password.html', success_url='done'), name='change_password'),
    path('setting/change_password/done', auth_views.PasswordChangeDoneView.as_view(template_name='change_password_done.html'), name='change_password_done'),
    path('account', views.UpdateAccountView.as_view(), name='my_account')
    ]
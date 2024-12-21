from django.urls import path
from accounts.views import *
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    # login
    path('logout', logout_view, name='logout'),
    # logout
    path('signup', signup_view, name='signup'),
    # registration / signup
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]

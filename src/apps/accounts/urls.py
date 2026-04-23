from django.urls import path

from apps.accounts.views import LoginView, RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='platform-user-register'),
    path('login/', LoginView.as_view(), name='platform-user-login'),
]

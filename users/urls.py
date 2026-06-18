from django.urls import path
from . import views
import uuid
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('register/',views.Registerview.as_view()),
    path('login/',views.Loginview.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='login_refresh'),
    path('profile/',views.ProfileView.as_view()),
    path('delete/<uuid:id>/',views.manage_account),
    path('become-provider/', views.BecomeProviderView.as_view()),
    path('providers/', views.list_providers, name='list_providers'),
    
]
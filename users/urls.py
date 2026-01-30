from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.Registerview.as_view()),
    path('login/',views.Loginview.as_view()),
    path('profile/',views.Profileview.as_view()),
]
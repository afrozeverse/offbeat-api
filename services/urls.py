from django.urls import path
from . import views

urlpatterns = [
    path('get-services/<uuid:place_id>/', views.get_services,name='getService'),
    path('create-service/', views.create_service,name='createService'),
    path('update-service/<uuid:id>/', views.update_service,name='updateService'),
    path('delete-service/<uuid:id>/', views.delete_service,name='deleteService'),
]